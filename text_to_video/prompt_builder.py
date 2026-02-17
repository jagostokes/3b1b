"""Prompt composition system for building tiered prompts from modular components."""

from pathlib import Path
from typing import List

# Prompt module directory
PROMPT_DIR = Path(__file__).parent / "prompts"


def _load_module(module_path: str) -> str:
    """Load a prompt module from file.

    Args:
        module_path: Relative path like 'core/hard_rules.md'

    Returns:
        Module content as string
    """
    full_path = PROMPT_DIR / module_path
    if not full_path.exists():
        raise FileNotFoundError(f"Prompt module not found: {full_path}")
    return full_path.read_text().strip()


def compose_prompt(tier: str, modules: List[str] = None, task: str = None) -> str:
    """Compose a prompt from modular components based on tier and task.

    Args:
        tier: Prompt tier - "minimal", "standard", or "detailed"
        modules: Optional explicit list of module paths to include
        task: Optional task type for specialized prompts

    Returns:
        Composed prompt string
    """
    if modules:
        # Explicit module list provided
        parts = [_load_module(m) for m in modules]
        return "\n\n".join(parts)

    # Default tier-based composition
    if tier == "minimal":
        # Syntax fixes, quick edits (250 lines)
        module_list = [
            "core/hard_rules.md",
            "rules/spatial_core.md",
            "reference/api_quick.md",
        ]
        if task:
            module_list.append(f"specialized/{task}.md")

    elif tier == "standard":
        # Initial code generation (600 lines)
        module_list = [
            "core/hard_rules.md",
            "core/teaching_principles.md",
            "rules/spatial_core.md",
            "rules/timing_formula.md",
            "reference/api_full.md",
        ]

    elif tier == "detailed":
        # Complex scenes, post-failure (800 lines)
        module_list = [
            "core/hard_rules.md",
            "core/teaching_principles.md",
            "core/output_format.md",
            "rules/spatial_core.md",
            "rules/timing_formula.md",
            "rules/temporal_core.md",
            "reference/api_full.md",
            "reference/patterns.md",
        ]

    else:
        raise ValueError(f"Unknown tier: {tier}. Use 'minimal', 'standard', or 'detailed'.")

    parts = [_load_module(m) for m in module_list]
    return "\n\n".join(parts)


def build_system_prompt(tier: str = "standard", task: str = None) -> str:
    """Build a complete system prompt with preamble + composed modules.

    Args:
        tier: Prompt tier - "minimal", "standard", or "detailed"
        task: Optional specialized task

    Returns:
        Complete system prompt
    """
    preamble = """You are a world-class manimgl video creator — the kind that makes 3Blue1Brown-quality educational animations.

You receive a plain-text description and produce a structured plan followed by complete, runnable Python code.

**CRITICAL**: This is 3b1b's **manimgl**, NOT ManimCE (Community Edition). The APIs differ significantly.

---
"""

    composed = compose_prompt(tier, task=task)
    return preamble + composed


def build_fix_prompt(error_type: str = None) -> str:
    """Build a specialized fix prompt based on error type.

    Args:
        error_type: Error category - "syntax", "api", "spatial", or "timing"

    Returns:
        Specialized fix prompt
    """
    base = """You are an expert manimgl debugger. You will receive a manimgl script that failed to render and the error message.

Fix the code so it runs successfully. Return ONLY the fixed Python code — no markdown fences, no explanations.

---
"""

    if error_type:
        specialized = _load_module(f"specialized/{error_type}_fixer.md")
        return base + specialized

    # General fix prompt (use standard tier)
    general = compose_prompt("standard")
    return base + general


def classify_error(error_msg: str, code: str) -> str:
    """Classify error type from error message and code.

    Uses multi-stage classification with confidence scoring.

    Args:
        error_msg: Error message from renderer
        code: Code that failed

    Returns:
        Error category: "syntax", "api", "spatial", "timing", or "general"
    """
    error_lower = error_msg.lower()

    # Stage 1: Python syntax/runtime errors (highest confidence)
    if any(kw in error_msg for kw in ["NameError", "AttributeError", "TypeError", "IndentationError", "SyntaxError", "KeyError", "IndexError", "ValueError"]):
        # Check if it's actually an API issue
        if any(api_kw in error_msg for api_kw in ["Create", "MathTex", "Tex", "camera.frame"]):
            return "api"

        # Handle AttributeError specifically
        if "AttributeError" in error_msg:
            # Check for Text.set_value (common mistake - wrong object type, not API issue)
            # Be flexible with quote characters
            if ("Text" in error_msg and "set_value" in error_msg):
                return "syntax"  # It's a syntax error (wrong method on object)
            # Check code for API patterns (camera, LaTeX, etc.)
            if any(api_kw in code for api_kw in ["self.camera.frame", "Tex(", "Create("]):
                return "api"
            # Otherwise, it's a syntax error (wrong attribute/method)
            return "syntax"

        # All other Python errors are syntax
        return "syntax"

    # Stage 2: Import errors (could be API or syntax)
    if "ImportError" in error_msg or "ModuleNotFoundError" in error_msg:
        if any(api_kw in error_msg for api_kw in ["Tex", "MathTex", "latex"]):
            return "api"
        return "syntax"

    # Stage 3: API-specific errors
    # Check code for wrong API usage
    api_issues = [
        "Create(",  # Should be ShowCreation
        "MathTex",  # Should be Text with Unicode
        "Tex(",     # Should be Text
        "TexText",  # Should be Text
        "self.camera.frame",  # ManimCE API
        "direction=",  # Wrong param for FadeIn
        ".animate(",  # Should be .animate.method()
    ]
    if any(issue in code for issue in api_issues):
        return "api"

    # Stage 4: Manimgl-specific errors
    if any(kw in error_lower for kw in ["manimlib", "mobject", "vmobject", "scene"]):
        # Could be API or spatial
        if any(kw in error_lower for kw in ["overlap", "position", "bounds", "off screen"]):
            return "spatial"
        return "api"

    # Stage 5: Spatial/layout errors (from checker or visual inspection)
    spatial_keywords = [
        "overlap", "overlapping", "collision", "off-screen", "off screen",
        "bounds", "frame", "too close", "same position", "alignment",
        "label on line", "text on shape", "crowded", "clipping"
    ]
    if any(kw in error_lower for kw in spatial_keywords):
        return "spatial"

    # Stage 6: Timing/pacing errors (from checker or user feedback)
    timing_keywords = [
        "too fast", "too slow", "missing wait", "duration", "pacing",
        "rushed", "timing", "wait time", "run_time"
    ]
    if any(kw in error_lower for kw in timing_keywords):
        return "timing"

    # Stage 7: Check for common patterns in code
    # Missing clear_updaters before FadeOut
    if "FadeOut" in code and "add_updater" in code and "clear_updaters" not in code:
        return "syntax"  # Temporal consistency issue

    # Multiple text at same position
    if code.count(".to_edge(DOWN)") > 1 and "FadeTransform" not in code:
        return "spatial"

    # Default: general
    return "general"


def classify_error_with_confidence(error_msg: str, code: str) -> tuple[str, float, dict]:
    """Classify error with confidence score and extracted patterns.

    Args:
        error_msg: Error message from renderer
        code: Code that failed

    Returns:
        Tuple of (error_type, confidence, details)
        - error_type: "syntax", "api", "spatial", "timing", or "general"
        - confidence: 0.0-1.0 score
        - details: Dictionary with extracted patterns
    """
    error_type = classify_error(error_msg, code)
    details = {}

    # Extract specific error patterns
    if error_type == "syntax":
        # Extract the specific error name
        for error_name in ["NameError", "AttributeError", "TypeError", "SyntaxError", "IndentationError"]:
            if error_name in error_msg:
                details["error_name"] = error_name
                # Extract the problematic variable/attribute
                if "name '" in error_msg:
                    start = error_msg.find("name '") + 6
                    end = error_msg.find("'", start)
                    details["undefined_name"] = error_msg[start:end]
                # Special case: Text.set_value is a well-known mistake
                if "'Text'" in error_msg and "set_value" in error_msg:
                    details["issue"] = "Text.set_value() doesn't exist (use DecimalNumber)"
                break
        confidence = 0.95

    elif error_type == "api":
        # Identify which API mistake
        if "Create(" in code:
            details["issue"] = "Create() instead of ShowCreation()"
            confidence = 1.0
        elif "MathTex" in code or "Tex(" in code:
            details["issue"] = "LaTeX usage (not installed)"
            confidence = 1.0
        elif "self.camera.frame" in code:
            details["issue"] = "ManimCE camera API"
            confidence = 1.0
        else:
            details["issue"] = "Unknown API mismatch"
            confidence = 0.7

    elif error_type == "spatial":
        # Count potential overlap sources
        overlap_count = code.count(".to_edge(DOWN)")
        if overlap_count > 1:
            details["issue"] = f"Multiple text at same edge ({overlap_count})"
            confidence = 0.9
        # Check for explicit overlap keywords
        elif any(kw in error_msg.lower() for kw in ["overlap", "same position", "collision"]):
            details["issue"] = "Explicit overlap detected"
            confidence = 0.85
        # Check for bounds/off-screen keywords
        elif any(kw in error_msg.lower() for kw in ["bounds", "off-screen", "off screen"]):
            details["issue"] = "Out of bounds"
            confidence = 0.85
        else:
            details["issue"] = "Potential spatial overlap"
            confidence = 0.6

    elif error_type == "timing":
        # Check for missing waits
        wait_count = code.count("self.wait(")
        play_count = code.count("self.play(")
        if play_count > 0:
            wait_ratio = wait_count / play_count
            details["wait_ratio"] = wait_ratio
            if wait_ratio < 0.3:
                details["issue"] = f"Too few waits ({wait_count}/{play_count} plays)"
                confidence = 0.85
            else:
                details["issue"] = "Timing issue"
                confidence = 0.6
        # Check for explicit timing keywords
        if any(kw in error_msg.lower() for kw in ["too fast", "too slow", "duration mismatch"]):
            details["issue"] = "Explicit timing issue"
            confidence = 0.75
        elif play_count == 0:
            confidence = 0.5

    else:  # general
        details["issue"] = "Could not classify"
        confidence = 0.3

    return error_type, confidence, details


def extract_error_context(error_msg: str, code: str) -> dict:
    """Extract contextual information from error message and code.

    Args:
        error_msg: Error message from renderer
        code: Code that failed

    Returns:
        Dictionary with extracted context
    """
    context = {
        "error_line": None,
        "error_type": None,
        "code_snippet": None,
        "traceback_depth": 0,
    }

    # Extract line number
    import re
    line_match = re.search(r'line (\d+)', error_msg)
    if line_match:
        context["error_line"] = int(line_match.group(1))

        # Extract code snippet around error line
        lines = code.split('\n')
        line_num = context["error_line"] - 1  # 0-indexed
        if 0 <= line_num < len(lines):
            start = max(0, line_num - 2)
            end = min(len(lines), line_num + 3)
            context["code_snippet"] = '\n'.join(
                f"{i+1}: {lines[i]}" for i in range(start, end)
            )

    # Extract error type
    error_type_match = re.search(r'(\w+Error)', error_msg)
    if error_type_match:
        context["error_type"] = error_type_match.group(1)

    # Count traceback depth
    context["traceback_depth"] = error_msg.count("File ")

    # Extract file name if present
    file_match = re.search(r'File "([^"]+)"', error_msg)
    if file_match:
        context["file"] = file_match.group(1)

    return context


def suggest_fix_strategy(error_type: str, confidence: float, details: dict) -> str:
    """Suggest a fix strategy based on error classification.

    Args:
        error_type: Classified error type
        confidence: Confidence score
        details: Extracted error details

    Returns:
        Strategy description
    """
    if confidence < 0.5:
        return "general_retry"  # Low confidence, use full context

    if error_type == "syntax":
        if "undefined_name" in details:
            return "variable_fix"  # Focus on variable definitions
        return "syntax_fix"

    elif error_type == "api":
        if "LaTeX" in details.get("issue", ""):
            return "latex_replacement"  # Specific: replace Tex with Text
        return "api_fix"

    elif error_type == "spatial":
        if "Multiple text" in details.get("issue", ""):
            return "fadetransform_fix"  # Specific: use FadeTransform
        return "spatial_fix"

    elif error_type == "timing":
        if "Too few waits" in details.get("issue", ""):
            return "add_waits"  # Specific: add self.wait() calls
        return "timing_fix"

    return "general_retry"


# Convenience functions for common prompts

def build_planner_prompt() -> str:
    """Build a planner prompt for single-pass pipeline."""
    preamble = """You are a master educational video planner for manimgl (3Blue1Brown's animation library).

Your role: convert the user's topic into a fully specified, execution-ready animation plan for a 3Blue1Brown-style video.

---
"""
    modules = [
        "core/teaching_principles.md",
        "rules/spatial_core.md",
        "rules/timing_formula.md",
        "reference/api_quick.md",
    ]
    composed = compose_prompt(tier="standard", modules=modules)

    output_format = """
---

OUTPUT FORMAT (follow exactly):

TITLE: <video title>

ACT 1: <name> (~Xs)
- Goal: <what this act teaches>
- Mobjects: <specific objects with colors>
- Animations: <step-by-step sequence with timing>
- Cleanup: <what gets FadeOut'd>

ACT 2: ...

CLOSING: (~Xs)
- Final message: <summary text>
- Cleanup: fade everything

TOTAL: ~Xs
"""

    return preamble + composed + output_format


def build_coder_prompt(mode: str = "single_pass") -> str:
    """Build a coder prompt for code generation.

    Args:
        mode: "single_pass" or "multi_pass"

    Returns:
        Coder prompt
    """
    if mode == "single_pass":
        preamble = """You are the Coding LLM in a multi-stage pipeline: Planner → **Coder** ↔ Checker → Render

You receive a detailed scene plan. Implement it as complete, runnable manimgl code — faithfully, precisely, without deviation.

---
"""
    else:  # multi_pass
        preamble = """You are generating code for a SINGLE ACT of a multi-act video.

OUTPUT RULES:
- Return ONLY raw Python code — NO class definition, NO imports
- Code at zero indent level (will be indented into construct() later)
- Use self.play(), self.wait(), self.add(), self.remove()

---
"""

    composed = compose_prompt("detailed")  # Full details for code generation

    rules = """
---

CODE GENERATION RULES:
1. Follow plan EXACTLY — positions, timing, colors, teaching goals
2. Class MUST be `GeneratedScene(Scene)` starting with `from manimlib import *`
3. Match timing: if plan says "~8s", your run_time + wait MUST sum to ~8s
4. Spatial precision: use exact coordinates/regions from plan
5. ZERO OVERLAP: text never sits on shapes, lines, axes, or other text
6. Clear ALL updaters before any FadeOut
7. Return ONLY runnable Python code — no markdown fences, no explanations
"""

    return preamble + composed + rules


def build_checker_prompt() -> str:
    """Build a checker prompt for code validation."""
    preamble = """You are the Checking LLM in a multi-stage pipeline: Planner → Coder ↔ **Checker** → Render

You receive the scene plan and generated code. Verify the code faithfully implements the plan with:
- Zero spatial collisions (no overlapping text/labels)
- Zero stale objects (all cleaned up)
- Correct API usage

---
"""

    modules = [
        "core/hard_rules.md",
        "rules/spatial_core.md",
        "rules/timing_formula.md",
        "rules/temporal_core.md",
    ]
    composed = compose_prompt(tier="standard", modules=modules)

    response_format = """
---

RESPONSE FORMAT:

If code passes ALL checks:
APPROVED

If code has issues:
ISSUES FOUND

1. [CATEGORY]: <specific problem>
   Location: <line/section>
   Expected: <what should happen>
   Actual: <what code does>
   Fix: <exact change needed>

2. ...

Priority: OVERLAPS > HARD RULE violations > temporal issues > API errors
"""

    return preamble + composed + response_format


# Prebuilt prompts for backward compatibility
SYSTEM_PROMPT_MINIMAL = build_system_prompt("minimal")
SYSTEM_PROMPT_STANDARD = build_system_prompt("standard")
SYSTEM_PROMPT_DETAILED = build_system_prompt("detailed")
