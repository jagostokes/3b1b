# API ERROR FIXER

Fix wrong API usage (ManimCE vs manimgl differences, wrong constructors).

## Common API Mistakes

### 1. Create() vs ShowCreation()

```python
# ❌ WRONG - ManimCE
self.play(Create(line))

# ✅ RIGHT - manimgl
self.play(ShowCreation(line))
```

### 2. LaTeX Classes (NOT AVAILABLE)

```python
# ❌ WRONG - LaTeX not installed
equation = MathTex("x^2 + y^2 = r^2")
text = TexText("Hello")

# ✅ RIGHT - Use Text() with Unicode
equation = Text("x² + y² = r²", font_size=36)
text = Text("Hello", font_size=48)
```

### 3. Animation Parameter Names

```python
# ❌ WRONG - ManimCE style
FadeIn(mob, direction=UP)
mob.animate(rotate=PI/2)

# ✅ RIGHT - manimgl style
FadeIn(mob, shift=UP * 0.3)
self.play(mob.animate.rotate(PI/2))
```

### 4. Arrow Constructor

```python
# ❌ WRONG - ManimCE parameters
Arrow(start, end, max_tip_length_to_length_ratio=0.3)

# ✅ RIGHT - manimgl parameters
Arrow(start, end, buff=0.25, tip_length=0.35)
```

### 5. Camera Frame (2D scenes)

```python
# ❌ WRONG - ManimCE 3D camera
self.camera.frame.move_to(point)

# ✅ RIGHT - manimgl 2D
# Don't manipulate camera in 2D scenes
# Position objects directly instead
```

## API Reference Quick Check

| ManimCE (WRONG)           | manimgl (RIGHT)              |
|---------------------------|------------------------------|
| `Create()`                | `ShowCreation()`             |
| `MathTex()`, `Tex()`      | `Text()` with Unicode        |
| `FadeIn(direction=UP)`    | `FadeIn(shift=UP*0.3)`       |
| `mob.animate(rotate=...)`| `mob.animate.rotate(...)`    |
| `self.camera.frame`       | Don't use (2D scenes)        |

## Fix Strategy

1. **Identify the wrong API** — check error message or code review
2. **Replace with manimgl equivalent** — see table above
3. **Check constructor parameters** — ensure correct argument names
4. **Verify method chaining** — `.animate.method()` not `.animate(method=)`
5. **Return ONLY fixed code** — no explanations
