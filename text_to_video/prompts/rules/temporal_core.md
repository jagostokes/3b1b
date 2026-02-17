# TEMPORAL CONSISTENCY (object lifecycle management)

## Object Lifecycle

```
Created → Added to scene → Animated → [Updated] → Updaters cleared → Faded out/Removed
```

## Cleanup Rules

1. **Track everything**: Every mobject must eventually be faded out or transformed
2. **Clear updaters BEFORE transitions**: `.clear_updaters()` before any `FadeOut`
3. **Group for cleanup**: `self.play(FadeOut(VGroup(a, b, c)))` at end of each act
4. **No orphaned objects**: Screen should be empty at end of each act

## Transform Semantics

| Transform type                      | What happens                                    | When to use            |
|-------------------------------------|-------------------------------------------------|------------------------|
| `Transform(a, b)`                   | `a` morphs to look like `b`, `a` stays in scene | When reusing `a` later |
| `ReplacementTransform(a, b)`        | `a` removed, `b` added                          | When working with `b`  |
| `FadeTransform(old, new)`           | Cross-fade morph, `old` removed, `new` added    | Text/label morphs      |

**CRITICAL**: After `Transform(a, b)`, FadeOut `a`, NOT `b` (b was never added)

## Updater Safety

```python
# Add updater
label.add_updater(lambda m: m.next_to(dot, UP, buff=0.1))

# ALWAYS clear before transition
label.clear_updaters()
self.play(FadeOut(label), run_time=0.4)
```
