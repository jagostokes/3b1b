# TIMING ERROR FIXER

Fix pacing issues: videos too fast, missing waits, duration mismatches.

## Common Timing Problems

### Problem 1: Missing self.wait() After Text

```python
# ❌ WRONG - no pause, viewer can't read
title = Text("Derivatives", font_size=60)
self.play(FadeIn(title, scale=0.8), run_time=1)
self.play(title.animate.scale(0.5).to_edge(UP), run_time=0.8)

# ✅ RIGHT - pause for viewer to read
title = Text("Derivatives", font_size=60)
self.play(FadeIn(title, scale=0.8), run_time=1)
self.wait(1.5)  # CRITICAL: narrator reads title
self.play(title.animate.scale(0.5).to_edge(UP), run_time=0.8)
```

**Fix strategy:**
- Add `self.wait(1.5)` after title appears
- Add `self.wait(1.0)` after new text labels
- Add `self.wait(0.5)` after complex animations
- Add `self.wait(0.5)` between acts

### Problem 2: Act Duration Doesn't Match Plan

```python
# Plan says: "Act 2 (~10s)"
# But code runs: 5s animation + 0.5s wait = 5.5s total

# ❌ WRONG - duration mismatch
self.play(ShowCreation(graph), run_time=2)
self.play(FadeIn(label), run_time=0.5)
self.wait(0.5)
# Total: 3.0s (should be ~10s!)

# ✅ RIGHT - match plan duration
self.play(ShowCreation(axes), run_time=1.5)
self.wait(0.5)
self.play(ShowCreation(graph), run_time=1.5)
self.wait(1.0)
self.play(FadeIn(label, shift=UP * 0.3), run_time=0.8)
self.wait(1.5)
# Total: 6.8s (closer to target)
```

**Fix strategy:**
- Sum all `run_time` + `self.wait()` values
- Compare to plan duration
- Add longer waits or slower `run_time` to match

### Problem 3: Video Too Fast (< 30s total)

```python
# ❌ WRONG - rushed, no breathing space
# 5 acts × 3s each = 15s total (too fast!)

# ✅ RIGHT - proper pacing
# Target: 35-45s total
# 4-6 acts × 7-10s each
# 80% animation, 20% wait

# Act timing formula:
# act_duration = setup (0.8-1.5s) + main (1.5-3.0s) + transition (0.6-0.8s) + pauses (1.0-2.0s)
```

**Fix strategy:**
- Target: 7-10s per act
- Target: 35-45s total video
- If under 30s, add more waits
- Slow down `run_time` for key animations (2-4s instead of 1s)

### Problem 4: No Pauses Between Steps

```python
# ❌ WRONG - animations back-to-back, overwhelming
self.play(ShowCreation(a))
self.play(ShowCreation(b))
self.play(ShowCreation(c))
self.play(ShowCreation(d))

# ✅ RIGHT - breathing space between steps
self.play(ShowCreation(a), run_time=1.0)
self.wait(0.5)
self.play(ShowCreation(b), run_time=1.0)
self.wait(0.5)
self.play(ShowCreation(c), run_time=1.0)
self.wait(1.0)  # Longer pause before key insight
self.play(ShowCreation(d), run_time=1.0)
self.wait(1.5)
```

**Fix strategy:**
- Add `self.wait(0.5)` between animations
- Add longer waits (1.0-2.0s) before key insights

## Timing Reference Table

| After...               | Minimum wait |
|------------------------|--------------|
| Title appears          | 1.5s         |
| New text label         | 1.0s         |
| Complex animation      | 0.5s         |
| Between acts           | 0.5s         |
| Before closing message | 2.0s         |
| After closing message  | 2.0s         |

## Act Duration Formula

```
act_duration = setup + main + transition + pauses
setup: 0.8-1.5s
main: 1.5-3.0s
transition: 0.6-0.8s
pauses: 1.0-2.0s
```

## Fix Workflow

1. **Calculate current total time** — sum all run_time + wait values
2. **Compare to target** — 7-10s per act, 35-45s total
3. **Add missing waits** — see table above
4. **Slow down key animations** — increase `run_time` for important reveals
5. **Return ONLY fixed code** — no explanations
