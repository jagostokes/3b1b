# COMPLETE MANIMGL API REFERENCE

## Text & Numbers

```python
Text(text, font_size=48, color=WHITE, font="", slant=NORMAL, weight=NORMAL,
     t2c={"substr": COLOR}, t2f={"substr": "Font"}, t2s={"substr": ITALIC}, t2w={"substr": BOLD})
  .set_color(color), .set_opacity(alpha), .set_width(w), .set_height(h)
  .set_backstroke(width=5)  # Dark outline for readability

DecimalNumber(number=0, num_decimal_places=2, font_size=48, color=WHITE)
  .set_value(new_val), .get_value(), .increment_value(delta)

Integer(number=0, font_size=48, color=WHITE)
```

## Coordinate Systems

```python
Axes(x_range=(-8, 8, 1), y_range=(-4, 4, 1), width=10, height=6,
     axis_config=dict(stroke_color=GREY_A, stroke_width=2))
  .c2p(x, y)  # Coordinates to point
  .p2c(point)  # Point to coordinates
  .i2gp(x, graph)  # Input x to graph point
  .get_graph(func, x_range=None, color=BLUE, use_smoothing=True)
  .get_tangent_line(x, graph, length=5)
  .slope_of_tangent(x, graph) → float
  .get_v_line(point), .get_h_line(point)
  .get_riemann_rectangles(graph, x_range=None, dx=0.5, colors=(BLUE, GREEN))
  .get_area_under_graph(graph, x_range=None, fill_color=BLUE, fill_opacity=0.5)
  .add_coordinate_labels(font_size=20, num_decimal_places=0)
  .get_origin()

NumberPlane(x_range=(-10, 10), y_range=(-5, 5))
  # Inherits all Axes methods
  .prepare_for_nonlinear_transform()  # Call before .apply_function()

NumberLine(x_range=(-8, 8, 1), unit_size=1.0, include_numbers=False)
  .number_to_point(x) / .n2p(x)
  .point_to_number(point) / .p2n(point)
```

## Shapes & Geometry

```python
Dot(point=ORIGIN, color=WHITE, radius=0.08)
SmallDot(point=ORIGIN, radius=0.04)
Line(start=LEFT, end=RIGHT, color=WHITE)
DashedLine(start, end, dash_length=0.05)
Arrow(start=LEFT, end=RIGHT, buff=0.25, tip_length=0.35)
Vector(direction=RIGHT, buff=0, color=YELLOW)  # Arrow from ORIGIN
Circle(radius=1.0, color=WHITE)
Arc(start_angle=0, angle=TAU/4, radius=1.0)
Ellipse(width=2, height=1)
Square(side_length=2.0)
Rectangle(width=2.0, height=1.0)
RoundedRectangle(width=4, height=2, corner_radius=0.5)
Polygon(*vertices)  # E.g., Polygon(UP, DL, DR) for triangle
RegularPolygon(n=6)  # Hexagon
Triangle()
SurroundingRectangle(mobject, buff=0.15, color=YELLOW)
Brace(mobject, direction=DOWN, buff=0.2)
  .get_tip(), .get_text(*text_args), .put_at_tip(mob)
```

## Grouping

```python
VGroup(*mobjects)
  .arrange(direction=RIGHT, buff=0.25)
  .arrange_in_grid(n_rows, n_cols, buff=0.25)
  [index], for mob in group: ...
```

## Universal Mobject Methods

```python
# Positioning
.move_to(point_or_mob), .next_to(mob, direction, buff=0.25)
.to_edge(direction, buff=0.5), .to_corner(direction, buff=0.5)
.shift(vector), .align_to(mob, direction), .center()

# Getters
.get_center(), .get_top(), .get_bottom(), .get_left(), .get_right()
.get_corner(direction)  # Works on rotated objects (UL, UR, DL, DR)
.get_start(), .get_end()  # For Line/Arrow
.get_width(), .get_height()

# Transforms
.scale(factor), .stretch(factor, dim)  # dim: 0=x, 1=y, 2=z
.rotate(angle, axis=OUT, about_point=None)
.flip(axis=UP), .set_width(w), .set_height(h)
.apply_matrix(matrix), .apply_function(func)

# Style
.set_color(color), .set_fill(color, opacity), .set_stroke(color, width, opacity)
.set_opacity(alpha), .copy()

# The .animate builder
mob.animate.shift(UP).set_color(RED)  # Use inside self.play()
```

## Updaters & ValueTracker

```python
ValueTracker(value=0)
  .get_value() → float
  .set_value(new_val) → self
  .animate.set_value(target)  # For animated changes

# Updater patterns
mob.add_updater(lambda m: m.next_to(dot, UP, buff=0.1))
mob.clear_updaters()  # CRITICAL before transitions
mob.remove_updater(func)

always_redraw(lambda: axes.get_h_line(dot.get_left()))
```

## Animations — Creation

```python
ShowCreation(mob, lag_ratio=1, run_time=1)  # Draw strokes
Uncreate(mob)  # Reverse
Write(mob)  # Border then fill (text)
DrawBorderThenFill(mob, run_time=2)
```

## Animations — Fading

```python
FadeIn(mob, shift=ORIGIN, scale=1, run_time=1)
FadeOut(mob, shift=ORIGIN, run_time=0.4)
VFadeIn(mob), VFadeOut(mob)  # Opacity-only
```

## Animations — Transforms

```python
Transform(source, target)  # Source morphs, stays in scene
ReplacementTransform(source, target)  # Source removed, target added
FadeTransform(source, target)  # Cross-fade morph (text)
TransformFromCopy(source, target)  # Copy morphs
ApplyMethod(mob.method, *args)
MoveToTarget(mob)  # Requires mob.generate_target(); mob.target.shift(UP)
```

## Animations — Growing & Indication

```python
GrowFromCenter(mob), GrowFromEdge(mob, edge), GrowArrow(arrow)
Indicate(mob, scale_factor=1.2, color=YELLOW, run_time=0.5)
Flash(point, color=YELLOW, run_time=0.3)
CircleIndicate(mob, color=YELLOW)
ShowCreationThenFadeOut(mob)
ShowPassingFlash(mob, time_width=0.1)
```

## Animations — Composition

```python
AnimationGroup(*anims, lag_ratio=0)
LaggedStart(*anims, lag_ratio=0.05)
LaggedStartMap(AnimClass, group, lag_ratio=0.1)
Succession(*anims)  # Play one after another
```

## Animations — Numbers

```python
ChangeDecimalToValue(decimal_mob, target_number, run_time=1)
CountInFrom(decimal_mob, source_number=0)
```

## Scene Methods

```python
self.play(*animations, run_time=1, rate_func=smooth)
self.wait(duration=1)
self.add(*mobjects)
self.remove(*mobjects)
self.clear()
self.bring_to_front(*mobs), self.bring_to_back(*mobs)
```

## Rate Functions

```
smooth, linear, rush_into, rush_from, double_smooth
there_and_back, wiggle, running_start, overshoot, lingering
```

## Constants

```python
# Directions
UP = [0, 1, 0], DOWN = [0, -1, 0], LEFT = [-1, 0, 0], RIGHT = [1, 0, 0]
UL, UR, DL, DR, ORIGIN, OUT, IN

# Buffs
SMALL_BUFF = 0.1, MED_SMALL_BUFF = 0.25, MED_LARGE_BUFF = 0.5, LARGE_BUFF = 1.0

# Colors (each has _A-_E variants)
BLUE, GREEN, YELLOW, RED, WHITE, ORANGE, PURPLE, PINK, TEAL, GOLD, GREY_A

# Math
PI, TAU, DEG (1 degree in radians)

# Frame
FRAME_WIDTH ≈ 14.2, FRAME_HEIGHT = 8.0
```

## Unicode Math Symbols

```
Superscripts: ² (\u00b2)  ³ (\u00b3)  ⁴ (\u2074)  ⁿ (\u207f)
Subscripts: ₀ (\u2080)  ₁ (\u2081)  ₂ (\u2082)  ₙ (\u2099)
Greek lower: α (\u03b1)  β (\u03b2)  γ (\u03b3)  δ (\u03b4)  ε (\u03b5)
             θ (\u03b8)  λ (\u03bb)  μ (\u03bc)  π (\u03c0)  σ (\u03c3)
             φ (\u03c6)  ω (\u03c9)
Greek upper: Γ (\u0393)  Δ (\u0394)  Σ (\u03a3)  Φ (\u03a6)  Ω (\u03a9)
Operators: × (\u00d7)  ÷ (\u00f7)  ± (\u00b1)  ≠ (\u2260)  ≤ (\u2264)  ≥ (\u2265)
           ≈ (\u2248)  ≡ (\u2261)
Calculus: ∫ (\u222b)  ∂ (\u2202)  ∇ (\u2207)  ∞ (\u221e)  Σ (\u2211)  Π (\u220f)
          ′ (\u2032)  ″ (\u2033)
Arrows: → (\u2192)  ← (\u2190)  ↔ (\u2194)  ⇒ (\u21d2)  ⇔ (\u21d4)
Sets: ∈ (\u2208)  ∉ (\u2209)  ⊂ (\u2282)  ∪ (\u222a)  ∩ (\u2229)  ∅ (\u2205)
Misc: √ (\u221a)  … (\u2026)  ⋅ (\u22c5)
```

## Utility Functions

```python
normalize(vect)  # Unit vector
get_norm(vect)  # Magnitude
get_dist(v1, v2)  # Distance
midpoint(p1, p2)
angle_of_vector(v)  # Radians
rotate_vector(v, angle, axis=OUT)
interpolate(start, end, alpha)  # Linear interpolation
```
