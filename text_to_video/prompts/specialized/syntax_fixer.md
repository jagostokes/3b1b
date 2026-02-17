# SYNTAX ERROR FIXER

Fix NameError, AttributeError, TypeError, and other Python syntax issues.

## Common Syntax Fixes

### NameError Fixes

```python
# ❌ WRONG
self.play(ShowCreation(grpah))  # Typo: grpah → graph

# ✅ RIGHT
self.play(ShowCreation(graph))
```

**Check:**
- Variable names match their definitions
- No typos in variable names
- Variables defined before use
- Correct imports present

### AttributeError Fixes

```python
# ❌ WRONG
text_obj.set_value(5)  # Text has no .set_value()

# ✅ RIGHT
# Use DecimalNumber or Integer for numbers
num_obj = DecimalNumber(5)
num_obj.set_value(10)
```

**Common mistakes:**
- `.set_value()` on Text → use DecimalNumber/Integer
- `font_size=` on shapes → only Text accepts font_size
- `.get_bottom()` on rotated objects → use `.get_corner()`
- `normalize()` on zero vector → add guard: `if get_norm(v) > 0.001:`

### TypeError Fixes

```python
# ❌ WRONG - wrong parameter names
FadeIn(mob, direction=UP)  # Should be shift=

# ✅ RIGHT
FadeIn(mob, shift=UP * 0.3)

# ❌ WRONG - wrong argument types
Arrow(start, end, max_tip_length_to_length_ratio=0.3)  # ManimCE API

# ✅ RIGHT - manimgl API
Arrow(start, end, buff=0.25, tip_length=0.35)
```

## Fix Strategy

1. **Read the error message carefully** — it tells you the line number and issue
2. **Check the line** — look for typos, undefined variables, wrong method calls
3. **Verify API usage** — ensure using manimgl, not ManimCE
4. **Test variable scope** — ensure variables exist in the current context
5. **Return ONLY the fixed code** — no explanations, no markdown fences
