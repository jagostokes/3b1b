"""CLI entry point and pipeline orchestration."""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

from .llm import (
    fix_code,
    generate_plan,
    generate_scene_code,
    check_scene_code,
    sp_generate_plan,
    sp_generate_code,
    sp_check_code,
    sp_fix_code,
)
from .renderer import Renderer, RenderResult, REPO_ROOT
from .player import play_video


def parse_plan_into_acts(plan: str) -> list[dict]:
    """
    Parse plan into structured acts.
    Returns: [{"name": "...", "duration": "...", "description": "..."}, ...]
    """
    acts = []
    lines = plan.split("\n")
    current_act = None

    for line in lines:
        line = line.strip()
        # Match "ACT N: Name (~Xs)" or "CLOSING: (~Xs)"
        act_match = re.match(r"^(ACT \d+|CLOSING):\s*(.+?)\s*\(~(\d+)s\)", line)
        if act_match:
            if current_act:
                acts.append(current_act)
            act_type = act_match.group(1)
            name = act_match.group(2) if act_type.startswith("ACT") else "Closing"
            duration = act_match.group(3)
            current_act = {
                "name": name,
                "duration": duration,
                "description": "",
            }
        elif current_act and line:
            # Accumulate description
            current_act["description"] += line + "\n"

    if current_act:
        acts.append(current_act)

    return acts


def multi_pass_pipeline(description: str, verbose: bool = False) -> tuple[str, str]:
    """
    Multi-pass pipeline with checker loop.
    Flow: plan → per-act code gen (enhanced prompt) ↔ check/regen → collate
    Returns: (plan, final_code)
    """
    # Step 1: Generate plan
    print("  [1/4] Generating plan...")
    plan = generate_plan(description)
    if verbose:
        print(f"\n--- PLAN ---\n{plan}\n--- END PLAN ---\n")

    # Step 2: Parse plan into acts
    acts = parse_plan_into_acts(plan)
    print(f"  [2/4] Plan has {len(acts)} acts to implement")

    # Step 3: Generate code for each act with checker loop
    scene_codes = []
    prior_context = "# This is ACT 1 — no prior context yet."

    for i, act in enumerate(acts, 1):
        print(f"\n  [3/4] Generating Act {i}: {act['name']}")
        max_attempts = 3
        approved = False
        act_code = ""

        for attempt in range(1, max_attempts + 1):
            print(f"    Attempt {attempt}/{max_attempts}...")

            # Generate code for this act using enhanced prompt
            act_code = generate_scene_code(
                act_description=act["description"],
                act_number=i,
                act_name=act["name"],
                full_plan=plan,
                prior_context=prior_context,
            )

            if verbose:
                print(f"\n--- ACT {i} CODE (attempt {attempt}) ---")
                print(act_code)
                print("--- END CODE ---\n")

            # Check the code
            approved, feedback = check_scene_code(act_code, act["description"])

            if approved:
                print(f"    ✓ Act {i} approved!")
                break
            else:
                print(f"    ✗ Issues found:")
                print(f"      {feedback[:200]}...")
                if attempt < max_attempts:
                    print(f"    Regenerating with feedback...")
                    # Add feedback to act description for next attempt
                    act["description"] += f"\n\nPREVIOUS ATTEMPT HAD ISSUES:\n{feedback}\nFix these issues."

        if not approved:
            print(f"    ⚠ Act {i} not fully approved after {max_attempts} attempts, using last version")

        scene_codes.append(act_code)

        # Update prior context for next act
        prior_context = f"# Previous acts created these variables:\n{act_code}\n"

    # Step 4: Coalate all scene codes
    print(f"\n  [4/4] Coalating {len(scene_codes)} acts into final scene...")

    # Combine all acts into final code
    final_code = "from manimlib import *\n\n"
    final_code += "class GeneratedScene(Scene):\n"
    final_code += "    def construct(self):\n"

    for i, act_code in enumerate(scene_codes, 1):
        # Remove any imports from individual acts
        act_code_clean = "\n".join(
            line for line in act_code.split("\n")
            if not line.strip().startswith("from ") and not line.strip().startswith("import ")
        )
        # Indent each line
        indented = "\n".join(f"        {line}" if line.strip() else "" for line in act_code_clean.split("\n"))
        final_code += f"\n        # ── Act {i}: {acts[i-1]['name']} ───────────────\n"
        final_code += indented
        final_code += "\n"

    return plan, final_code


def single_pass_pipeline(description: str, verbose: bool = False) -> tuple[str, str]:
    """
    Single-pass pipeline: Planner → Coder ↔ Checker → final code.
    Flow: plan entire video → generate full scene → check/fix loop → return.
    Returns: (plan, final_code)
    """
    # Step 1: Generate plan
    print("  [1/3] Planning scene...")
    plan = sp_generate_plan(description)
    if verbose:
        print(f"\n--- PLAN ---\n{plan}\n--- END PLAN ---\n")

    # Step 2: Generate code from plan
    print("  [2/3] Generating code from plan...")
    code = sp_generate_code(plan)
    if verbose:
        print(f"\n--- CODE ---\n{code}\n--- END CODE ---\n")

    # Step 3: Check and fix loop
    max_checks = 2
    for check in range(1, max_checks + 1):
        print(f"  [3/3] Checking code (round {check}/{max_checks})...")
        approved, feedback = sp_check_code(code, plan)

        if approved:
            print("    ✓ Code approved!")
            break

        print(f"    ✗ Issues found:")
        print(f"      {feedback[:300]}...")

        if check < max_checks:
            print("    Fixing code with feedback...")
            code = sp_fix_code(plan, code, feedback)
            if verbose:
                print(f"\n--- FIXED CODE ---\n{code}\n--- END FIXED CODE ---\n")

    return plan, code


def main():
    parser = argparse.ArgumentParser(
        description="Generate a manim video from a text description."
    )
    parser.add_argument(
        "input",
        help="Path to a .txt file or a quoted description string.",
    )
    parser.add_argument(
        "--no-play",
        action="store_true",
        help="Skip auto-playing the video after rendering.",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output directory name (default: timestamped).",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print the plan and generated code.",
    )
    parser.add_argument(
        "--multi-pass",
        action="store_true",
        help="Use multi-pass pipeline with checker bot (slower but higher quality).",
    )
    args = parser.parse_args()

    # Read input — treat as file path only if it looks like one and exists
    try:
        input_path = Path(args.input)
        is_file = len(args.input) < 260 and input_path.is_file()
    except OSError:
        is_file = False

    if is_file:
        description = input_path.read_text().strip()
    else:
        description = args.input

    if not description:
        print("Error: empty description.", file=sys.stderr)
        sys.exit(1)

    # Create output directory
    if args.output:
        output_dir = REPO_ROOT / "output" / args.output
    else:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = REPO_ROOT / "output" / stamp

    renderer = Renderer(output_dir)
    print(f"Output: {output_dir}")

    # Step 1: Generate plan + code
    if args.multi_pass:
        print("[1/3] Generating scene with multi-pass pipeline...")
        plan, code = multi_pass_pipeline(description, verbose=args.verbose)
    else:
        print("[1/3] Generating scene (Planner → Coder → Checker)...")
        plan, code = single_pass_pipeline(description, verbose=args.verbose)

    renderer.save_plan(plan)
    if args.verbose:
        print("\n--- PLAN ---")
        print(plan)
        print("--- END PLAN ---\n")
        print("--- CODE ---")
        print(code)
        print("--- END CODE ---\n")

    # Step 2: Render with retry
    result = RenderResult(success=False, video_path=None, error_msg="")
    max_attempts = 3

    for attempt in range(1, max_attempts + 1):
        print(f"[2/3] Rendering (attempt {attempt}/{max_attempts})...")
        scene_file = renderer.write_scene(code, attempt)
        result = renderer.render(scene_file)

        if result.success:
            print(f"  Render succeeded! Video: {result.video_path}")
            break

        print(f"  Render failed. Error:\n{result.error_msg[:500]}")
        if attempt < max_attempts:
            print("  Asking LLM to fix the code...")
            code = fix_code(code, result.error_msg, use_enhanced=True)
            if args.verbose:
                print(f"\n--- FIXED CODE (attempt {attempt + 1}) ---")
                print(code)
                print("--- END FIXED CODE ---\n")

    if not result.success:
        print(
            f"\nFailed to render after {max_attempts} attempts.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Step 3: Play
    if not args.no_play and result.video_path:
        print("[3/3] Opening video...")
        play_video(result.video_path)
    elif result.video_path:
        print(f"[3/3] Video saved at: {result.video_path}")

    print("Done.")


if __name__ == "__main__":
    main()
