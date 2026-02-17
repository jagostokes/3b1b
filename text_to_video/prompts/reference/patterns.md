# COPY-PASTE PATTERNS & RECIPES

## Pattern A: Title Card → Shrink to Top

```python
title = Text("My Topic", font_size=60)
self.play(FadeIn(title, scale=0.8), run_time=1)
self.wait(1.5)
self.play(title.animate.scale(0.5).to_edge(UP), run_time=0.8)
```

## Pattern B: Axes + Graph + Label

```python
axes = Axes(x_range=(-3, 4, 1), y_range=(-1, 10, 2), width=10, height=6)
axes.shift(0.5 * DOWN)
axes.add_coordinate_labels(font_size=18)

graph = axes.get_graph(lambda x: x**2, x_range=(-3, 3.3), color=BLUE)
graph.set_stroke(width=3)

label = Text("f(x) = x²", font_size=30, color=BLUE)
label.next_to(axes.i2gp(2.8, graph), UR, buff=0.3)

self.play(ShowCreation(axes), run_time=1.5)
self.play(ShowCreation(graph), run_time=1.5)
self.play(FadeIn(label, shift=UP * 0.3), run_time=0.8)
self.wait(1.5)
```

## Pattern C: Sliding Dot with ValueTracker

```python
x_tracker = ValueTracker(1)
dot = Dot(axes.i2gp(1, graph), color=YELLOW, radius=0.07)
dot.add_updater(lambda d: d.move_to(axes.i2gp(x_tracker.get_value(), graph)))

self.play(FadeIn(dot, scale=0.5), run_time=0.5)
self.play(x_tracker.animate.set_value(-2), run_time=2.5)
self.play(x_tracker.animate.set_value(3), run_time=4)

dot.clear_updaters()  # ALWAYS before transitioning
```

## Pattern D: Dynamic Perpendicular Positioning

```python
# Place objects perpendicular to a line (works for ANY orientation)
side_vector = end_point - start_point
perpendicular = normalize(np.array([-side_vector[1], side_vector[0], 0]))

# Calculate perpendicular offset dynamically (NEVER hardcode UP/DOWN/LEFT/RIGHT)
label.move_to(line_center + perpendicular * 0.5)

# For squares on triangle sides (precise vertex calculation)
side_length = get_norm(side_vector)
perp_scaled = perpendicular * side_length  # MUST normalize first
C = point_B + perp_scaled
D = point_A + perp_scaled
square = Polygon(point_A, point_B, C, D, color=BLUE, fill_opacity=0.3)
```

## Pattern E: Clean Act Transition

```python
# End of Act — gather all objects and fade out together
act_objects = VGroup(axes, graph, label, dot, title)
self.play(FadeOut(act_objects), run_time=1)
self.wait(0.5)

# Next act starts fresh
subtitle = Text("Part 2: Analysis", font_size=50)
self.play(FadeIn(subtitle, scale=0.8), run_time=1)
```

## Pattern F: Staggered Group Reveal

```python
items = VGroup(
    Text("Point 1", font_size=30),
    Text("Point 2", font_size=30),
    Text("Point 3", font_size=30),
).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
items.to_edge(LEFT, buff=1)

self.play(
    LaggedStart(*[FadeIn(item, shift=RIGHT * 0.5) for item in items], lag_ratio=0.3),
    run_time=2,
)
self.wait(2)
```

## Pattern G: Tangent Line with Live Slope Readout

```python
x_tracker = ValueTracker(1)
tangent = axes.get_tangent_line(1, graph, length=4).set_color(GREEN)
tangent.add_updater(
    lambda t: t.become(
        axes.get_tangent_line(x_tracker.get_value(), graph, length=4).set_color(GREEN)
    )
)

slope_label = Text("slope = ", font_size=28, color=GREEN)
slope_num = DecimalNumber(
    axes.slope_of_tangent(1, graph), num_decimal_places=2, font_size=28, color=GREEN
)
slope_group = VGroup(slope_label, slope_num).arrange(RIGHT, buff=0.1)
slope_group.to_corner(UR, buff=0.5)
slope_num.add_updater(
    lambda s: s.set_value(axes.slope_of_tangent(x_tracker.get_value(), graph))
)

self.play(ShowCreation(tangent), FadeIn(slope_group), run_time=1)
self.play(x_tracker.animate.set_value(3), run_time=4)

tangent.clear_updaters()
slope_num.clear_updaters()
```

## Pattern H: Secant → Tangent Limit

```python
x0 = 1.0
h_tracker = ValueTracker(2.0)

dot_a = Dot(axes.i2gp(x0, graph), color=YELLOW, radius=0.07)
dot_b = Dot(axes.i2gp(x0 + 2, graph), color=YELLOW, radius=0.07)

def build_secant(h):
    pa = axes.i2gp(x0, graph)
    pb = axes.i2gp(x0 + h, graph)
    direction = normalize(pb - pa)
    return Line(pa - direction * 1.5, pb + direction * 1.5, color=RED)

secant = build_secant(2.0)
secant.add_updater(lambda l: l.become(build_secant(h_tracker.get_value())))
dot_b.add_updater(lambda d: d.move_to(axes.i2gp(x0 + h_tracker.get_value(), graph)))

self.play(FadeIn(dot_a), FadeIn(dot_b), ShowCreation(secant), run_time=1)
self.play(h_tracker.animate.set_value(0.01), run_time=3, rate_func=smooth)

secant.clear_updaters()
dot_b.clear_updaters()
```

## Pattern I: Riemann Sum Animation

```python
axes = Axes(x_range=(0, 5, 1), y_range=(0, 10, 2), width=10, height=6)
graph = axes.get_graph(lambda x: x**2, x_range=(0, 4), color=BLUE)

# Start with coarse rectangles
rects_coarse = axes.get_riemann_rectangles(graph, x_range=(0, 4), dx=1.0)
self.play(ShowCreation(rects_coarse), run_time=1.5)
self.wait(1)

# Refine to finer rectangles
rects_fine = axes.get_riemann_rectangles(graph, x_range=(0, 4), dx=0.25)
self.play(ReplacementTransform(rects_coarse, rects_fine), run_time=2)
self.wait(1)

# Show area
area = axes.get_area_under_graph(graph, x_range=(0, 4), fill_color=BLUE, fill_opacity=0.3)
self.play(FadeOut(rects_fine), FadeIn(area), run_time=1)
```

## Pattern J: TracedPath (Moving Dot Trail)

```python
dot = Dot(color=YELLOW)
dot.move_to(axes.c2p(0, 0))

trail = TracedPath(dot.get_center, stroke_color=YELLOW, stroke_width=2)
self.add(trail, dot)

# Animate the dot — trail follows automatically
self.play(dot.animate.move_to(axes.c2p(3, 2)), run_time=2)
self.play(dot.animate.move_to(axes.c2p(5, 0)), run_time=2)
```
