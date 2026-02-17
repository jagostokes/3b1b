# SPATIAL ERROR FIXER

Fix overlapping text, labels on lines, off-screen objects.

## Overlap Detection & Fixes

### Problem 1: Label Sitting on a Line

```python
# ❌ WRONG - label at line center (overlaps line)
label.next_to(line.get_center(), UP, buff=0.15)  # Too close!

# ✅ RIGHT - perpendicular offset, away from line
side_vec = line.get_end() - line.get_start()
perp = normalize(np.array([-side_vec[1], side_vec[0], 0]))
label.move_to(line.get_center() + perp * 0.5)  # 0.5 unit gap
```

**Fix strategy:**
- Calculate perpendicular to line dynamically
- Offset by ≥ 0.4 units
- Choose direction pointing AWAY from other geometry

### Problem 2: Multiple Text at Same Position

```python
# ❌ WRONG - two labels at bottom edge
eq1 = Text("a² + b²").to_edge(DOWN)
self.play(Write(eq1))
eq2 = Text("= c²").to_edge(DOWN)  # Overlaps eq1!
self.play(Write(eq2))

# ✅ RIGHT - replace, don't stack
eq1 = Text("a² + b²").to_edge(DOWN)
self.play(Write(eq1))
eq2 = Text("a² + b² = c²").to_edge(DOWN)
self.play(FadeTransform(eq1, eq2))  # eq1 removed, eq2 added
```

**Fix strategy:**
- ONE text per screen region at a time
- Use `FadeTransform(old, new)` to replace
- Or assign labels to different quadrants (UR, UL, DR, DL)

### Problem 3: Graph Label in Center (Overlaps Axes)

```python
# ❌ WRONG - label at curve midpoint (crosses axes/gridlines)
label.next_to(axes.i2gp(1.5, graph), UR, buff=0.2)

# ✅ RIGHT - label at curve ENDPOINT
label.next_to(axes.i2gp(2.8, graph), UR, buff=0.3)  # High x value
```

**Fix strategy:**
- Place graph labels at curve endpoints (high x)
- Avoid midpoints where axes cross

### Problem 4: Objects Off-Screen

```python
# ❌ WRONG - large triangle with squares goes off-screen
A = np.array([-4, -3, 0])
B = np.array([4, -3, 0])
C = np.array([-4, 3, 0])
# Squares built on this will exceed [-7, 7] × [-4, 4]

# ✅ RIGHT - start SMALL
A = np.array([-1.5, -1, 0])
B = np.array([1.5, -1, 0])
C = np.array([-1.5, 1, 0])
# Squares fit within safe zone [-6, 6] × [-3, 3]
```

**Fix strategy:**
- Frame bounds: ~14 × 8 units
- Safe content zone: [-6, 6] × [-3, 3]
- Start with SMALL shapes (sides 1-3 units)
- Scale up only if needed and verified to fit

### Problem 5: Right Angle Marker Floating

```python
# ❌ WRONG - marker not touching both sides
corner_marker = Square(side_length=0.3, color=WHITE)
corner_marker.move_to(A)  # Floating in space!

# ✅ RIGHT - align to corner direction
corner_marker = Square(side_length=0.3, color=WHITE)
corner_marker.move_to(A)
corner_marker.align_to(A, DL)  # Bottom-left corner touches A
```

**Fix strategy:**
- Use `.align_to(point, direction)` where direction = DL, DR, UL, or UR
- Ensures marker touches BOTH sides of the angle

## Minimum Distances (MANDATORY)

| Label near...      | Minimum offset |
|-------------------|----------------|
| Line or curve     | 0.4 units perpendicular |
| Another label     | 0.5 units apart |
| Axis              | 0.3 units |
| Screen edge       | 0.5 units (use `to_edge` default buff) |

## Fix Workflow

1. **Identify overlap source** — read error or visually inspect code
2. **Calculate safe position** — use perpendicular offsets, different quadrants
3. **Verify minimum distances** — check table above
4. **Use FadeTransform for text replacement** — don't stack
5. **Return ONLY fixed code** — no explanations
