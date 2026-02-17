# MANIMGL API QUICK REFERENCE (most-used objects and methods)

## Text & Numbers

```python
Text(string, font_size=48, color=WHITE, t2c={"substr": COLOR})
DecimalNumber(number=0, num_decimal_places=2, font_size=48)
  .set_value(new_val)  # Use in updaters
  .get_value()
Integer(number=0, font_size=48)
```

## Coordinate Systems

```python
Axes(x_range=(-8, 8, 1), y_range=(-4, 4, 1), width=10, height=6)
  .c2p(x, y)  # Coordinates to point
  .i2gp(x, graph)  # Input to graph point
  .get_graph(func, x_range=None, color=BLUE)
  .get_tangent_line(x, graph, length=5)
  .slope_of_tangent(x, graph)
  .add_coordinate_labels(font_size=20)
```

## Shapes

```python
Dot(point=ORIGIN, color=WHITE, radius=0.08)
Line(start, end, color=WHITE)
DashedLine(start, end, dash_length=0.05)
Arrow(start, end, buff=0.25, tip_length=0.35)
Circle(radius=1.0, color=WHITE)
Square(side_length=2.0)
Rectangle(width=2.0, height=1.0)
Polygon(*vertices)
```

## Essential Animations

```python
ShowCreation(mob, run_time=1.0)  # Draw strokes
FadeIn(mob, shift=ORIGIN, scale=1, run_time=1.0)
FadeOut(mob, run_time=0.4)
FadeTransform(old, new, run_time=0.8)  # Morph text
ReplacementTransform(source, target, run_time=0.8)
Indicate(mob, scale_factor=1.2, color=YELLOW, run_time=0.5)
GrowArrow(arrow, run_time=0.8)
LaggedStart(*anims, lag_ratio=0.3, run_time=2.0)
```

## Positioning Methods

```python
mob.move_to(point_or_mob)
mob.next_to(mob_or_point, direction, buff=0.25)
mob.to_edge(direction, buff=0.5)
mob.to_corner(direction, buff=0.5)
mob.shift(vector)
mob.get_center()
mob.get_corner(direction)  # Works on rotated objects
```

## The .animate Builder

```python
# Chain transformations inside self.play()
self.play(mob.animate.shift(UP).set_color(RED), run_time=1.5)
self.play(mob.animate.scale(2).move_to(ORIGIN))
```

## ValueTracker Pattern

```python
tracker = ValueTracker(0)
dot.add_updater(lambda d: d.move_to(axes.i2gp(tracker.get_value(), graph)))
self.play(tracker.animate.set_value(5), run_time=3)

# CRITICAL: Always clear before transitioning
dot.clear_updaters()
```

## Constants

```python
# Directions
UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR, ORIGIN

# Colors
BLUE, GREEN, YELLOW, RED, WHITE, ORANGE, PURPLE, GREY_A

# Math
PI, TAU, DEG

# Frame
FRAME_WIDTH ≈ 14.2, FRAME_HEIGHT = 8.0
```

## Unicode Math Symbols

```
Superscripts: ² ³ ⁴ ⁿ
Subscripts: ₀ ₁ ₂ ₙ
Greek: α β γ δ ε θ λ π σ τ φ ω
Operators: × ÷ ± ≠ ≤ ≥ ≈ ≡
Calculus: ∫ ∂ ∇ ∞ Σ ′ ″
Arrows: → ← ↔ ⇒ ⇔
Sets: ∈ ∉ ⊂ ∪ ∩ ∅
Misc: √ … ⋅
```
