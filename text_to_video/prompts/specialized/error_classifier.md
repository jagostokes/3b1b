# ERROR CLASSIFICATION

Categorize error types to route to specialized fix prompts.

## Error Categories

### Syntax Errors
- `NameError`: variable used before definition, misspelled name
- `AttributeError`: wrong method name, object doesn't have attribute
- `TypeError`: wrong argument names or types
- `IndentationError`: incorrect indentation
- `SyntaxError`: Python syntax violations

### API Errors
- `Create()` instead of `ShowCreation()`
- `Tex`, `MathTex`, `TexText` used instead of `Text()` with Unicode
- Wrong animation parameter names (`direction=` vs `shift=`)
- Wrong object constructors (ManimCE vs manimgl differences)

### Spatial Errors
- Labels overlapping lines, curves, axes
- Multiple text objects at same position
- Objects positioned off-screen (out of frame bounds)
- Right angle markers not aligned properly

### Timing Errors
- Missing `self.wait()` after text appears
- Act duration doesn't match plan
- Too many animations without pauses
- Video runs too fast (< 30s total)

## Routing Logic

```
if "NameError" in error or "AttributeError" in error:
    → syntax_fixer.md

elif "Create(" in code or "MathTex" in code or "Tex(" in code:
    → api_fixer.md

elif "overlap" in error or "off-screen" in error:
    → spatial_fixer.md

elif "too fast" in error or "missing wait" in error:
    → timing_fixer.md

else:
    → general fix (use full ENHANCED_PROMPT + FIX_CODE_PROMPT)
```
