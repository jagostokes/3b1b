#!/usr/bin/env python3
"""Test suite for error classification system with historical failure cases."""

from text_to_video.prompt_builder import (
    classify_error,
    classify_error_with_confidence,
    extract_error_context,
    suggest_fix_strategy,
)


# Historical failure cases collected from actual renders
HISTORICAL_FAILURES = [
    # Syntax errors
    {
        "name": "NameError: typo in variable",
        "error": "NameError: name 'grpah' is not defined",
        "code": "self.play(ShowCreation(grpah))",
        "expected_type": "syntax",
        "expected_confidence_min": 0.9,
    },
    {
        "name": "AttributeError: wrong method",
        "error": "AttributeError: 'Text' object has no attribute 'set_value'",
        "code": "text_obj = Text('hello')\ntext_obj.set_value(5)",
        "expected_type": "syntax",
        "expected_confidence_min": 0.9,
    },
    {
        "name": "TypeError: wrong argument",
        "error": "TypeError: FadeIn() got an unexpected keyword argument 'direction'",
        "code": "self.play(FadeIn(mob, direction=UP))",
        "expected_type": "syntax",
        "expected_confidence_min": 0.9,
    },
    {
        "name": "IndentationError",
        "error": "IndentationError: unexpected indent at line 15",
        "code": "def construct(self):\n    title = Text('test')\n      self.play(FadeIn(title))",
        "expected_type": "syntax",
        "expected_confidence_min": 0.9,
    },

    # API errors
    {
        "name": "Create instead of ShowCreation",
        "error": "NameError: name 'Create' is not defined",
        "code": "self.play(Create(line))",
        "expected_type": "api",
        "expected_confidence_min": 0.95,
    },
    {
        "name": "MathTex usage",
        "error": "ImportError: cannot import name 'MathTex'",
        "code": "equation = MathTex('x^2 + y^2 = r^2')",
        "expected_type": "api",
        "expected_confidence_min": 0.95,
    },
    {
        "name": "Tex usage",
        "error": "NameError: name 'Tex' is not defined",
        "code": "text = Tex('Hello')",
        "expected_type": "api",
        "expected_confidence_min": 0.95,
    },
    {
        "name": "Camera frame (ManimCE API)",
        "error": "AttributeError: 'Scene' object has no attribute 'camera'",
        "code": "self.camera.frame.move_to(point)",
        "expected_type": "api",
        "expected_confidence_min": 0.95,
    },

    # Spatial errors
    {
        "name": "Multiple text at same position",
        "error": "Visual check: two equations overlap at bottom",
        "code": """
eq1 = Text("a² + b²").to_edge(DOWN)
self.play(Write(eq1))
eq2 = Text("= c²").to_edge(DOWN)
self.play(Write(eq2))
""",
        "expected_type": "spatial",
        "expected_confidence_min": 0.8,
    },
    {
        "name": "Label on line",
        "error": "overlap detected: label sits on line",
        "code": "label.next_to(line.get_center(), UP, buff=0.1)",
        "expected_type": "spatial",
        "expected_confidence_min": 0.8,
    },
    {
        "name": "Off-screen object",
        "error": "bounds exceeded: object position off screen",
        "code": "square = Square(side_length=10).move_to(np.array([15, 15, 0]))",
        "expected_type": "spatial",
        "expected_confidence_min": 0.8,
    },

    # Timing errors
    {
        "name": "Missing waits",
        "error": "video too fast: missing wait after text",
        "code": """
title = Text("Test")
self.play(FadeIn(title))
self.play(title.animate.scale(0.5))
""",
        "expected_type": "timing",
        "expected_confidence_min": 0.7,
    },
    {
        "name": "Duration mismatch",
        "error": "act duration mismatch: plan says 10s, actual 5s",
        "code": "self.play(ShowCreation(graph), run_time=2)\nself.wait(0.5)",
        "expected_type": "timing",
        "expected_confidence_min": 0.7,
    },

    # Edge cases
    {
        "name": "Missing clear_updaters",
        "error": "RuntimeError: cannot remove object with active updaters",
        "code": """
dot.add_updater(lambda d: d.move_to(point))
self.play(FadeOut(dot))
""",
        "expected_type": "syntax",  # Temporal consistency issue
        "expected_confidence_min": 0.7,
    },
    {
        "name": "General unknown error",
        "error": "Unknown error occurred during rendering",
        "code": "some_random_code()",
        "expected_type": "general",
        "expected_confidence_min": 0.0,
    },
]


def test_error_classification():
    """Test error classification on historical failures."""
    print("=" * 80)
    print("ERROR CLASSIFICATION TEST SUITE")
    print("=" * 80)
    print()

    passed = 0
    failed = 0
    total = len(HISTORICAL_FAILURES)

    for i, case in enumerate(HISTORICAL_FAILURES, 1):
        name = case["name"]
        error = case["error"]
        code = case["code"]
        expected_type = case["expected_type"]
        expected_conf_min = case["expected_confidence_min"]

        # Basic classification
        result_type = classify_error(error, code)

        # Enhanced classification
        result_type_enhanced, confidence, details = classify_error_with_confidence(error, code)

        # Extract context
        context = extract_error_context(error, code)

        # Get strategy
        strategy = suggest_fix_strategy(result_type_enhanced, confidence, details)

        # Check if classification is correct
        type_match = result_type == expected_type
        conf_match = confidence >= expected_conf_min

        if type_match and conf_match:
            status = "✅ PASS"
            passed += 1
        else:
            status = "❌ FAIL"
            failed += 1

        print(f"Test {i}/{total}: {status}")
        print(f"  Name: {name}")
        print(f"  Expected: {expected_type} (conf >= {expected_conf_min:.1%})")
        print(f"  Got: {result_type_enhanced} (conf = {confidence:.1%})")
        print(f"  Strategy: {strategy}")

        if details:
            print(f"  Details: {details}")

        if not type_match:
            print(f"  ⚠️  Type mismatch!")
        if not conf_match:
            print(f"  ⚠️  Confidence too low!")

        print()

    # Summary
    print("=" * 80)
    print(f"RESULTS: {passed}/{total} passed, {failed}/{total} failed")
    print(f"Success rate: {passed/total*100:.1f}%")
    print("=" * 80)

    return passed, failed


def test_error_context_extraction():
    """Test error context extraction."""
    print()
    print("=" * 80)
    print("ERROR CONTEXT EXTRACTION TEST")
    print("=" * 80)
    print()

    test_cases = [
        {
            "name": "Extract line number",
            "error": 'File "scene.py", line 42, in construct\n    NameError: name "x" is not defined',
            "code": "line1\nline2\nline3",
            "expected_line": 42,
        },
        {
            "name": "Extract error type",
            "error": "AttributeError: object has no attribute 'foo'",
            "code": "code",
            "expected_error_type": "AttributeError",
        },
        {
            "name": "No line number",
            "error": "Generic error message",
            "code": "code",
            "expected_line": None,
        },
    ]

    passed = 0
    for case in test_cases:
        context = extract_error_context(case["error"], case["code"])

        if "expected_line" in case:
            if context["error_line"] == case["expected_line"]:
                print(f"✅ {case['name']}: Line {context['error_line']}")
                passed += 1
            else:
                print(f"❌ {case['name']}: Expected line {case['expected_line']}, got {context['error_line']}")

        if "expected_error_type" in case:
            if context["error_type"] == case["expected_error_type"]:
                print(f"✅ {case['name']}: Type {context['error_type']}")
                passed += 1
            else:
                print(f"❌ {case['name']}: Expected {case['expected_error_type']}, got {context['error_type']}")

    print()
    print(f"Context extraction: {passed}/{len(test_cases)} checks passed")
    print("=" * 80)


def test_fix_strategy_selection():
    """Test fix strategy selection."""
    print()
    print("=" * 80)
    print("FIX STRATEGY SELECTION TEST")
    print("=" * 80)
    print()

    test_cases = [
        {
            "error_type": "syntax",
            "confidence": 0.95,
            "details": {"undefined_name": "grpah"},
            "expected_strategy": "variable_fix",
        },
        {
            "error_type": "api",
            "confidence": 1.0,
            "details": {"issue": "LaTeX usage (not installed)"},
            "expected_strategy": "latex_replacement",
        },
        {
            "error_type": "spatial",
            "confidence": 0.9,
            "details": {"issue": "Multiple text at same edge (2)"},
            "expected_strategy": "fadetransform_fix",
        },
        {
            "error_type": "timing",
            "confidence": 0.85,
            "details": {"issue": "Too few waits (2/8 plays)", "wait_ratio": 0.25},
            "expected_strategy": "add_waits",
        },
        {
            "error_type": "general",
            "confidence": 0.3,
            "details": {},
            "expected_strategy": "general_retry",
        },
        {
            "error_type": "syntax",
            "confidence": 0.4,  # Low confidence
            "details": {},
            "expected_strategy": "general_retry",
        },
    ]

    passed = 0
    for case in test_cases:
        strategy = suggest_fix_strategy(
            case["error_type"],
            case["confidence"],
            case["details"]
        )

        if strategy == case["expected_strategy"]:
            print(f"✅ {case['error_type']} (conf={case['confidence']:.1%}): {strategy}")
            passed += 1
        else:
            print(f"❌ {case['error_type']}: Expected {case['expected_strategy']}, got {strategy}")

    print()
    print(f"Strategy selection: {passed}/{len(test_cases)} tests passed")
    print("=" * 80)


def main():
    """Run all tests."""
    passed, failed = test_error_classification()
    test_error_context_extraction()
    test_fix_strategy_selection()

    print()
    print("=" * 80)
    print("OVERALL TEST SUMMARY")
    print("=" * 80)
    print(f"Main classification tests: {passed}/{passed+failed} passed")

    if failed == 0:
        print("\n✅ All tests passed! Error classification system is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {failed} tests failed. Review error classification logic.")
        return 1


if __name__ == "__main__":
    exit(main())
