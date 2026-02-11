"""Grok/xAI LLM client using OpenAI-compatible API."""

import os
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

load_dotenv()


def _get_client() -> OpenAI:
    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "XAI_API_KEY not set. Add it to .env or export it in your shell."
        )
    return OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")


def _call(system: str, user: str, max_tokens: int = 16000) -> str:
    client = _get_client()
    response = client.chat.completions.create(
        model="grok-3-fast",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )
    return response.choices[0].message.content


def generate_scene(description: str) -> tuple[str, str]:
    """Single LLM call: returns (plan, code) parsed from the response."""
    raw = _call(SYSTEM_PROMPT, description)
    plan, code = _parse_response(raw)
    code = _strip_fences(code)
    return plan, code


def fix_code(code: str, error: str, use_enhanced: bool = False) -> str:
    """Send broken code + error to LLM, get back fixed code."""
    user_msg = (
        f"BROKEN CODE:\n```python\n{code}\n```\n\n"
        f"ERROR:\n{error}\n\n"
        "Fix the code and return ONLY the corrected Python code."
    )
    system = FIX_CODE_PROMPT
    if use_enhanced:
        system = ENHANCED_PROMPT + "\n\n" + FIX_CODE_PROMPT
    fixed = _call(system, user_msg)
    fixed = _strip_fences(fixed)
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
    plan = _call(PLANNER_PROMPT, description, max_tokens=4000)
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
    code = _call(SCENE_GENERATOR_PROMPT, user_msg, max_tokens=8000)
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
    response = _call(CHECKER_PROMPT, user_msg, max_tokens=4000)
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
    plan = _call(SP_PLANNER_PROMPT, description, max_tokens=4000)
    return plan.strip()


def sp_generate_code(plan: str) -> str:
    """Coder stage: scene plan → complete runnable scene code."""
    user_msg = (
        f"SCENE PLAN:\n\n{plan}\n\n"
        f"Generate the complete scene code following this plan exactly."
    )
    code = _call(SP_CODER_PROMPT, user_msg, max_tokens=16000)
    return _strip_fences(code)


def sp_check_code(code: str, plan: str) -> tuple[bool, str]:
    """Checker stage: code + plan → (approved, feedback)."""
    user_msg = (
        f"ORIGINAL PLAN:\n{plan}\n\n"
        f"CODE TO CHECK:\n```python\n{code}\n```"
    )
    response = _call(SP_CHECKER_PROMPT, user_msg, max_tokens=4000)
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
    code = _call(SP_CODER_PROMPT, user_msg, max_tokens=16000)
    return _strip_fences(code)
