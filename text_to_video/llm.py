"""Grok/xAI LLM client using OpenAI-compatible API."""

import os
import time
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

from .prompt import (
    SYSTEM_PROMPT,
    FIX_CODE_PROMPT,
    PLANNER_PROMPT,
    SCENE_GENERATOR_PROMPT,
    CHECKER_PROMPT,
    ENHANCED_PROMPT,
    SP_PLANNER_PROMPT,
    SP_CODER_PROMPT,
    SP_CHECKER_PROMPT,
)
from .prompt_builder import (
    build_fix_prompt,
    classify_error,
    classify_error_with_confidence,
    extract_error_context,
    suggest_fix_strategy,
)
from .metrics import VideoMetrics

load_dotenv()

# Global metrics tracker (set by cli.py when needed)
_current_metrics: Optional[VideoMetrics] = None


def set_metrics_tracker(metrics: VideoMetrics):
    """Set the global metrics tracker for this generation session."""
    global _current_metrics
    _current_metrics = metrics


def _get_client() -> OpenAI:
    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "XAI_API_KEY not set. Add it to .env or export it in your shell."
        )
    return OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")


def _call(system: str, user: str, max_tokens: int = 16000, purpose: str = "general") -> str:
    """Make an LLM API call with metrics tracking.

    Args:
        system: System prompt
        user: User message
        max_tokens: Maximum completion tokens
        purpose: Purpose of the call for metrics tracking

    Returns:
        LLM response content
    """
    client = _get_client()

    start_time = time.time()
    response = client.chat.completions.create(
        model="grok-3-fast",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )
    duration = time.time() - start_time

    # Track metrics if collector is active
    if _current_metrics:
        # Estimate token counts (OpenAI API provides usage, but xAI may not)
        prompt_tokens = response.usage.prompt_tokens if hasattr(response, 'usage') and response.usage else len(system.split()) + len(user.split())
        completion_tokens = response.usage.completion_tokens if hasattr(response, 'usage') and response.usage else len(response.choices[0].message.content.split())

        _current_metrics.add_llm_call(
            purpose=purpose,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            duration_seconds=duration,
        )

    return response.choices[0].message.content


def generate_scene(description: str) -> tuple[str, str]:
    """Single LLM call: returns (plan, code) parsed from the response."""
    raw = _call(SYSTEM_PROMPT, description, purpose="generate_scene")
    plan, code = _parse_response(raw)
    code = _strip_fences(code)
    return plan, code


def fix_code(code: str, error: str, use_enhanced: bool = False, verbose: bool = False) -> str:
    """Send broken code + error to LLM, get back fixed code.

    Uses enhanced error classification with confidence scoring to route to specialized fix prompts.

    Args:
        code: The broken code
        error: Error message from renderer
        use_enhanced: Force use of full enhanced prompt
        verbose: Print detailed error analysis

    Returns:
        Fixed code
    """
    # Enhanced classification with confidence
    error_type, confidence, details = classify_error_with_confidence(error, code)
    strategy = suggest_fix_strategy(error_type, confidence, details)
    context = extract_error_context(error, code)

    # Verbose output
    if verbose:
        print(f"\n  === Error Analysis ===")
        print(f"  Type: {error_type}")
        print(f"  Confidence: {confidence:.2%}")
        print(f"  Strategy: {strategy}")
        if details:
            print(f"  Details: {details}")
        if context.get("error_line"):
            print(f"  Error line: {context['error_line']}")
            if context.get("code_snippet"):
                print(f"  Context:\n{context['code_snippet']}")
        print(f"  ======================\n")
    else:
        print(f"  Error classified as: {error_type} (confidence: {confidence:.1%})")

    # Build user message with context
    user_msg = f"BROKEN CODE:\n```python\n{code}\n```\n\n"
    user_msg += f"ERROR:\n{error}\n\n"

    # Add extracted context for better fixes
    if context.get("error_line"):
        user_msg += f"ERROR LOCATION: Line {context['error_line']}\n"
    if context.get("code_snippet"):
        user_msg += f"CODE CONTEXT:\n{context['code_snippet']}\n\n"

    # Add specific guidance based on details
    if details:
        if "undefined_name" in details:
            user_msg += f"ISSUE: Variable '{details['undefined_name']}' is not defined. Check for typos or missing definitions.\n"
        elif "issue" in details:
            user_msg += f"LIKELY ISSUE: {details['issue']}\n"

    user_msg += "\nFix the code and return ONLY the corrected Python code."

    # Select prompt based on confidence and strategy
    if use_enhanced or confidence < 0.5 or error_type == "general":
        # Use full enhanced prompt for low-confidence or complex errors
        system = ENHANCED_PROMPT + "\n\n" + FIX_CODE_PROMPT
        print(f"  Using enhanced prompt (full context)")
    else:
        # Use specialized fix prompt
        system = build_fix_prompt(error_type)
        print(f"  Using specialized {error_type} fixer")

    # Make LLM call with appropriate purpose tag
    fixed = _call(system, user_msg, purpose=f"fix_{error_type}_{strategy}")
    fixed = _strip_fences(fixed)

    # Track detailed error info in metrics
    if _current_metrics:
        # Note: render attempt is tracked separately in cli.py
        # This just adds classification info
        pass

    return fixed


def _parse_response(raw: str) -> tuple[str, str]:
    """Split LLM response on === PLAN === and === CODE === delimiters."""
    plan = ""
    code = raw  # fallback: treat entire response as code

    if "=== PLAN ===" in raw and "=== CODE ===" in raw:
        after_plan = raw.split("=== PLAN ===", 1)[1]
        plan, code = after_plan.split("=== CODE ===", 1)
        plan = plan.strip()
        code = code.strip()
    elif "=== CODE ===" in raw:
        plan, code = raw.split("=== CODE ===", 1)
        plan = plan.strip()
        code = code.strip()

    return plan, code


def _strip_fences(code: str) -> str:
    """Remove markdown code fences if present."""
    code = code.strip()
    if code.startswith("```python"):
        code = code[len("```python"):]
    elif code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]
    return code.strip()


# ═════════════════════════════════════════════════════════════════════════════
# MULTI-PASS PIPELINE FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════


def generate_plan(description: str) -> str:
    """Generate a structured scene-by-scene plan."""
    plan = _call(PLANNER_PROMPT, description, max_tokens=4000, purpose="plan")
    return plan.strip()


def generate_scene_code(
    act_description: str,
    act_number: int,
    act_name: str,
    full_plan: str,
    prior_context: str,
) -> str:
    """Generate code for a single act using the enhanced prompt."""
    user_msg = (
        f"FULL VIDEO PLAN:\n{full_plan}\n\n"
        f"GENERATING ACT {act_number}: {act_name}\n\n"
        f"ACT DESCRIPTION:\n{act_description}\n\n"
        f"CONTEXT FROM PREVIOUS ACTS (variables already in scope):\n{prior_context}\n\n"
        f"Generate the Python code for this act only. Raw code, no markdown fences."
    )
    code = _call(SCENE_GENERATOR_PROMPT, user_msg, max_tokens=8000, purpose=f"code_act{act_number}")
    code = _strip_fences(code)
    return code


def check_scene_code(code: str, act_description: str) -> tuple[bool, str]:
    """
    Check code for issues.
    Returns (approved: bool, feedback: str).
    """
    user_msg = (
        f"CODE TO CHECK:\n```python\n{code}\n```\n\n"
        f"ACT DESCRIPTION:\n{act_description}"
    )
    response = _call(CHECKER_PROMPT, user_msg, max_tokens=4000, purpose="check")
    response = response.strip()

    if response.startswith("APPROVED"):
        return True, ""
    else:
        return False, response


# ═════════════════════════════════════════════════════════════════════════════
# SINGLE-PASS PIPELINE FUNCTIONS (Planner → Coder ↔ Checker)
# ═════════════════════════════════════════════════════════════════════════════


def sp_generate_plan(description: str) -> str:
    """Planner stage: user description → structured scene plan."""
    plan = _call(SP_PLANNER_PROMPT, description, max_tokens=4000, purpose="plan")
    return plan.strip()


def sp_generate_code(plan: str) -> str:
    """Coder stage: scene plan → complete runnable scene code."""
    user_msg = (
        f"SCENE PLAN:\n\n{plan}\n\n"
        f"Generate the complete scene code following this plan exactly."
    )
    code = _call(SP_CODER_PROMPT, user_msg, max_tokens=16000, purpose="code")
    return _strip_fences(code)


def sp_check_code(code: str, plan: str) -> tuple[bool, str]:
    """Checker stage: code + plan → (approved, feedback)."""
    user_msg = (
        f"ORIGINAL PLAN:\n{plan}\n\n"
        f"CODE TO CHECK:\n```python\n{code}\n```"
    )
    response = _call(SP_CHECKER_PROMPT, user_msg, max_tokens=4000, purpose="check")
    response = response.strip()

    if response.startswith("APPROVED"):
        return True, ""
    return False, response


def sp_fix_code(plan: str, code: str, feedback: str) -> str:
    """Coder stage with checker feedback: plan + code + feedback → fixed code."""
    user_msg = (
        f"SCENE PLAN:\n\n{plan}\n\n"
        f"CURRENT CODE:\n```python\n{code}\n```\n\n"
        f"CHECKER FEEDBACK (fix these issues):\n{feedback}\n\n"
        f"Fix all issues identified by the checker. Return the complete "
        f"corrected scene code."
    )
    code = _call(SP_CODER_PROMPT, user_msg, max_tokens=16000, purpose="fix_checker_feedback")
    return _strip_fences(code)
