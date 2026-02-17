# TIMING FORMULA (non-negotiable pacing rules)

## Act Duration Formula

```
act_duration = setup + main + transition + pauses
```

- **Setup animation**: 0.8-1.5s (axes, shapes, static elements)
- **Main animation**: 1.5-3.0s (key transformation, equation reveal)
- **Transition animation**: 0.6-0.8s (fades, label swaps)
- **Pauses**: 1.0-2.0s (viewer reads, narrator speaks)

## Wait Time Requirements

| After...               | Minimum wait |
|------------------------|--------------|
| Title appears          | 1.5s         |
| New text label         | 1.0s         |
| Complex animation      | 0.5s         |
| Between acts           | 0.5s         |
| Before closing message | 2.0s         |
| After closing message  | 2.0s         |

## Verification

**CRITICAL**: `sum(run_time + wait)` MUST match plan duration ±1s

Target ratio: **80% animation, 20% wait**

Example: 7s act = 5.6s animation + 1.4s wait
