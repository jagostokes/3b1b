# HARD RULES (non-negotiable — violating any causes build failure)

1. Class MUST be named `GeneratedScene` and extend `Scene`
2. File MUST start with `from manimlib import *`
3. NEVER use `Tex`, `TexText`, `MathTex` — LaTeX is NOT installed. Use `Text()` with Unicode
4. NEVER import packages beyond `manimlib`, `numpy`, `math`
5. NEVER use `self.embed()`, `self.interact()`, or interactive methods
6. NEVER use interactive widgets: `Textbox`, `Checkbox`, `ColorSliders`, `ControlPanel`
7. Return ONLY Python code — no markdown fences, no prose
8. NEVER use `Create()` — use `ShowCreation()` (manimgl API)
9. NEVER use `MathTex()` — use `Text()` with Unicode
10. NEVER use `self.camera.frame` for 2D scenes — different API from ManimCE
