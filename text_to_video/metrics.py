"""Metrics tracking for measuring prompt efficiency and quality improvements."""

import json
import time
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional


@dataclass
class LLMCall:
    """Record of a single LLM API call."""
    timestamp: str
    purpose: str  # "plan", "code", "check", "fix"
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    duration_seconds: float
    model: str = "grok-3-fast"


@dataclass
class RenderAttempt:
    """Record of a render attempt."""
    attempt_number: int
    success: bool
    error_type: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class VideoMetrics:
    """Complete metrics for a single video generation."""
    video_id: str  # Timestamp or output dir name
    description: str
    pipeline: str  # "single_pass" or "multi_pass"
    tier: str  # "minimal", "standard", or "detailed"

    # LLM metrics
    llm_calls: List[LLMCall] = field(default_factory=list)
    total_llm_calls: int = 0
    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0

    # Timing metrics
    start_time: str = ""
    end_time: str = ""
    total_duration_seconds: float = 0.0
    generation_duration_seconds: float = 0.0  # LLM only
    render_duration_seconds: float = 0.0

    # Render metrics
    render_attempts: List[RenderAttempt] = field(default_factory=list)
    total_render_attempts: int = 0
    first_pass_success: bool = False
    final_success: bool = False

    # Quality metrics (if available)
    spatial_errors: int = 0
    timing_errors: int = 0
    api_errors: int = 0

    def add_llm_call(
        self,
        purpose: str,
        prompt_tokens: int,
        completion_tokens: int,
        duration_seconds: float,
    ):
        """Record an LLM API call."""
        call = LLMCall(
            timestamp=datetime.now().isoformat(),
            purpose=purpose,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            duration_seconds=duration_seconds,
        )
        self.llm_calls.append(call)
        self.total_llm_calls += 1
        self.total_tokens += call.total_tokens
        self.prompt_tokens += prompt_tokens
        self.completion_tokens += completion_tokens
        self.generation_duration_seconds += duration_seconds

    def add_render_attempt(
        self,
        attempt_number: int,
        success: bool,
        error_type: Optional[str] = None,
        error_message: Optional[str] = None,
    ):
        """Record a render attempt."""
        attempt = RenderAttempt(
            attempt_number=attempt_number,
            success=success,
            error_type=error_type,
            error_message=error_message,
        )
        self.render_attempts.append(attempt)
        self.total_render_attempts += 1

        if attempt_number == 1 and success:
            self.first_pass_success = True

        if success:
            self.final_success = True

        # Count error types
        if error_type:
            if "spatial" in error_type.lower() or "overlap" in error_type.lower():
                self.spatial_errors += 1
            elif "timing" in error_type.lower():
                self.timing_errors += 1
            elif "api" in error_type.lower() or "syntax" in error_type.lower():
                self.api_errors += 1

    def finalize(self):
        """Calculate final metrics."""
        self.end_time = datetime.now().isoformat()
        if self.start_time and self.end_time:
            start = datetime.fromisoformat(self.start_time)
            end = datetime.fromisoformat(self.end_time)
            self.total_duration_seconds = (end - start).total_seconds()

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    def summary(self) -> str:
        """Generate human-readable summary."""
        lines = [
            f"=== VIDEO METRICS SUMMARY ===",
            f"Video ID: {self.video_id}",
            f"Pipeline: {self.pipeline}",
            f"Tier: {self.tier}",
            f"",
            f"LLM Metrics:",
            f"  Total calls: {self.total_llm_calls}",
            f"  Total tokens: {self.total_tokens:,}",
            f"  Prompt tokens: {self.prompt_tokens:,}",
            f"  Completion tokens: {self.completion_tokens:,}",
            f"  Generation time: {self.generation_duration_seconds:.1f}s",
            f"",
            f"Render Metrics:",
            f"  Total attempts: {self.total_render_attempts}",
            f"  First-pass success: {'✓' if self.first_pass_success else '✗'}",
            f"  Final success: {'✓' if self.final_success else '✗'}",
            f"",
            f"Error Breakdown:",
            f"  Spatial errors: {self.spatial_errors}",
            f"  Timing errors: {self.timing_errors}",
            f"  API errors: {self.api_errors}",
            f"",
            f"Timing:",
            f"  Total duration: {self.total_duration_seconds:.1f}s",
            f"  Generation: {self.generation_duration_seconds:.1f}s",
            f"  Rendering: {self.render_duration_seconds:.1f}s",
        ]
        return "\n".join(lines)


class MetricsCollector:
    """Context manager for collecting metrics during video generation."""

    def __init__(self, output_dir: Path, description: str, pipeline: str, tier: str):
        self.output_dir = output_dir
        self.metrics = VideoMetrics(
            video_id=output_dir.name,
            description=description[:200],  # Truncate long descriptions
            pipeline=pipeline,
            tier=tier,
            start_time=datetime.now().isoformat(),
        )
        self.render_start_time = None

    def __enter__(self):
        return self.metrics

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.metrics.finalize()
        self.save()

    def save(self):
        """Save metrics to JSON file."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        metrics_file = self.output_dir / "metrics.json"

        with open(metrics_file, "w") as f:
            json.dump(self.metrics.to_dict(), f, indent=2)

        # Also save summary as text
        summary_file = self.output_dir / "metrics_summary.txt"
        with open(summary_file, "w") as f:
            f.write(self.metrics.summary())


def compare_metrics(before_dir: Path, after_dir: Path) -> str:
    """Compare metrics from two video generations.

    Args:
        before_dir: Directory with old system metrics
        after_dir: Directory with new system metrics

    Returns:
        Comparison report as string
    """
    before_file = before_dir / "metrics.json"
    after_file = after_dir / "metrics.json"

    if not before_file.exists() or not after_file.exists():
        return "Error: metrics.json not found in one or both directories"

    with open(before_file) as f:
        before = json.load(f)
    with open(after_file) as f:
        after = json.load(f)

    def pct_change(old, new):
        if old == 0:
            return "N/A"
        change = ((new - old) / old) * 100
        sign = "+" if change > 0 else ""
        return f"{sign}{change:.1f}%"

    lines = [
        "=== METRICS COMPARISON ===",
        f"Before: {before['video_id']}",
        f"After: {after['video_id']}",
        "",
        "LLM Metrics:",
        f"  Total calls: {before['total_llm_calls']} → {after['total_llm_calls']} ({pct_change(before['total_llm_calls'], after['total_llm_calls'])})",
        f"  Total tokens: {before['total_tokens']:,} → {after['total_tokens']:,} ({pct_change(before['total_tokens'], after['total_tokens'])})",
        f"  Generation time: {before['generation_duration_seconds']:.1f}s → {after['generation_duration_seconds']:.1f}s ({pct_change(before['generation_duration_seconds'], after['generation_duration_seconds'])})",
        "",
        "Render Metrics:",
        f"  Total attempts: {before['total_render_attempts']} → {after['total_render_attempts']}",
        f"  First-pass success: {before['first_pass_success']} → {after['first_pass_success']}",
        "",
        "Error Breakdown:",
        f"  Spatial errors: {before['spatial_errors']} → {after['spatial_errors']}",
        f"  Timing errors: {before['timing_errors']} → {after['timing_errors']}",
        f"  API errors: {before['api_errors']} → {after['api_errors']}",
        "",
        "Overall Improvement:",
    ]

    # Calculate improvement score
    token_reduction = (before['total_tokens'] - after['total_tokens']) / before['total_tokens'] * 100 if before['total_tokens'] > 0 else 0
    call_reduction = (before['total_llm_calls'] - after['total_llm_calls']) / before['total_llm_calls'] * 100 if before['total_llm_calls'] > 0 else 0
    time_reduction = (before['total_duration_seconds'] - after['total_duration_seconds']) / before['total_duration_seconds'] * 100 if before['total_duration_seconds'] > 0 else 0

    lines.append(f"  Token reduction: {token_reduction:.1f}%")
    lines.append(f"  Call reduction: {call_reduction:.1f}%")
    lines.append(f"  Time reduction: {time_reduction:.1f}%")

    if token_reduction >= 30 and (after['first_pass_success'] or before['first_pass_success'] == after['first_pass_success']):
        lines.append("")
        lines.append("✅ Target improvements met! (30%+ token reduction, quality maintained)")
    else:
        lines.append("")
        lines.append("❌ Target not met. Need 30%+ token reduction with maintained quality.")

    return "\n".join(lines)


def batch_compare(metrics_dir: Path, baseline_pattern: str = "baseline_*", improved_pattern: str = "improved_*"):
    """Compare metrics across multiple video pairs.

    Args:
        metrics_dir: Directory containing metric JSON files
        baseline_pattern: Glob pattern for baseline videos
        improved_pattern: Glob pattern for improved videos

    Returns:
        Aggregate comparison report
    """
    baseline_files = list(metrics_dir.glob(f"{baseline_pattern}/metrics.json"))
    improved_files = list(metrics_dir.glob(f"{improved_pattern}/metrics.json"))

    if not baseline_files or not improved_files:
        return "Error: No matching metric files found"

    total_token_before = 0
    total_token_after = 0
    total_calls_before = 0
    total_calls_after = 0
    first_pass_before = 0
    first_pass_after = 0

    for bf, af in zip(sorted(baseline_files), sorted(improved_files)):
        with open(bf) as f:
            before = json.load(f)
        with open(af) as f:
            after = json.load(f)

        total_token_before += before['total_tokens']
        total_token_after += after['total_tokens']
        total_calls_before += before['total_llm_calls']
        total_calls_after += after['total_llm_calls']
        if before['first_pass_success']:
            first_pass_before += 1
        if after['first_pass_success']:
            first_pass_after += 1

    num_videos = len(baseline_files)
    token_reduction = (total_token_before - total_token_after) / total_token_before * 100 if total_token_before > 0 else 0
    call_reduction = (total_calls_before - total_calls_after) / total_calls_before * 100 if total_calls_before > 0 else 0

    report = f"""=== BATCH METRICS COMPARISON ===
Videos analyzed: {num_videos}

Aggregate Results:
  Total tokens (before): {total_token_before:,}
  Total tokens (after): {total_token_after:,}
  Token reduction: {token_reduction:.1f}%

  Total LLM calls (before): {total_calls_before}
  Total LLM calls (after): {total_calls_after}
  Call reduction: {call_reduction:.1f}%

  First-pass success (before): {first_pass_before}/{num_videos} ({first_pass_before/num_videos*100:.1f}%)
  First-pass success (after): {first_pass_after}/{num_videos} ({first_pass_after/num_videos*100:.1f}%)

Target Evaluation:
  ✅ Token reduction >= 30%: {token_reduction >= 30}
  ✅ Quality improvement >= 15%: {(first_pass_after - first_pass_before) / num_videos * 100 >= 15 if num_videos > 0 else False}
"""

    return report
