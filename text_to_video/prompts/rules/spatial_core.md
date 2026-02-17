# SPATIAL RULES (MANDATORY — no overlap, precise positioning)

## Frame Dimensions

- Frame: ~14.2 × ~8 units (`FRAME_WIDTH` × `FRAME_HEIGHT`)
- Safe content zone: [-6, 6] × [-3, 3]
- Start with SMALL shapes if building on them (sides 1-3 units)

## Mandatory Minimum Distances

| Label near...      | Minimum offset |
|-------------------|----------------|
| Line or curve     | 0.4 units perpendicular |
| Another label     | 0.5 units apart |
| Axis              | 0.3 units |
| Screen edge       | 0.5 units |

## Screen Region Assignments (ONE text per region at a time)

- **Top band (y ≥ 3.0)**: title only
- **Center (x ∈ [-3, 3])**: main geometry (axes, shapes, graphs)
- **Corners (UR, UL, DR, DL)**: persistent labels (one per corner)
- **Bottom (y ≤ -3)**: equations (ONE at a time — use FadeTransform to replace)

## Anti-Overlap Checklist

- [ ] NO text overlays any line, curve, axis, or shape edge
- [ ] NO two text labels at same position
- [ ] Graph labels at curve ENDPOINTS, not midpoints
- [ ] Line labels: perpendicular offset ≥ 0.4 units (NEVER on the line)
- [ ] Right angle markers touch BOTH sides (use `.align_to(corner, DL)`)
- [ ] Squares on triangle sides: exact shared vertices, not rotated approximations

## REPLACE, DON'T STACK

Two labels at same position → `FadeTransform(old, new)` — never stack text
