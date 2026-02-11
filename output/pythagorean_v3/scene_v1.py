from manimlib import *

class GeneratedScene(Scene):
    def construct(self):
        # Act 1: Hook - Distance Without Measuring (~8s)
        grid = NumberPlane(x_range=(-5, 5), y_range=(-3, 3), width=10, height=6)
        grid.shift(0.5 * DOWN)
        point1 = Dot(grid.c2p(-3, -2), color=YELLOW, radius=0.07)
        point2 = Dot(grid.c2p(2, 1), color=YELLOW, radius=0.07)
        stair_h = Line(grid.c2p(-3, -2), grid.c2p(2, -2), color=RED)
        stair_v = Line(grid.c2p(2, -2), grid.c2p(2, 1), color=RED)
        diagonal = Line(grid.c2p(-3, -2), grid.c2p(2, 1), color=GREEN)
        question = Text("Shortest path?", font_size=30, color=WHITE)
        question.next_to(diagonal.get_center(), UR, buff=0.2)

        self.play(FadeIn(grid), FadeIn(point1, scale=0.5), FadeIn(point2, scale=0.5), run_time=1)
        self.play(ShowCreation(stair_h), run_time=1.5)
        self.play(ShowCreation(stair_v), run_time=1.5)
        self.play(ShowCreation(diagonal), Indicate(diagonal, color=GREEN), run_time=1.5)
        self.play(FadeIn(question, shift=UP * 0.3), run_time=0.8)
        self.wait(1.7)

        # Act 2: Right Triangle Emerges (~8s)
        A = grid.c2p(-3, -2)
        B = grid.c2p(2, -2)
        C = grid.c2p(2, 1)
        side_a = Line(B, C, color=BLUE)
        side_b = Line(A, B, color=GREEN)
        side_c = Line(A, C, color=RED)
        right_angle_marker = Square(side_length=0.3, color=WHITE)
        right_angle_marker.move_to(B)
        right_angle_marker.align_to(B, DL)
        label_a = Text("a", font_size=30, color=BLUE)
        label_b = Text("b", font_size=30, color=GREEN)
        label_c = Text("c", font_size=30, color=RED)
        label_a.next_to(side_a.get_center(), RIGHT, buff=0.2)
        label_b.next_to(side_b.get_center(), DOWN, buff=0.2)
        label_c.next_to(side_c.get_center(), UL, buff=0.2)

        self.play(FadeOut(stair_h), FadeOut(stair_v), run_time=0.5)
        self.play(ShowCreation(side_a), ShowCreation(side_b), ShowCreation(side_c), run_time=1.5)
        self.play(ShowCreation(right_angle_marker), run_time=0.8)
        self.play(Indicate(side_a), FadeIn(label_a, shift=UP * 0.3), run_time=1)
        self.play(Indicate(side_b), FadeIn(label_b, shift=UP * 0.3), run_time=1)
        self.play(Indicate(side_c), FadeIn(label_c, shift=UP * 0.3), run_time=1)
        self.wait(2.2)

        # Act 3: Build Squares on Each Side (~10s)
        # Square on side a (BC, outward)
        side_a_vec = C - B
        perp_a = np.array([-side_a_vec[1], side_a_vec[0], 0])
        centroid = (A + B + C) / 3
        if np.dot(perp_a, centroid - side_a.get_center()) < 0:
            perp_a = -perp_a
        P_a1 = B + perp_a
        P_a2 = C + perp_a
        square_a = Polygon(B, C, P_a2, P_a1, color=BLUE, fill_opacity=0.3, stroke_width=2)

        # Square on side b (AB, outward)
        side_b_vec = B - A
        perp_b = np.array([-side_b_vec[1], side_b_vec[0], 0])
        if np.dot(perp_b, centroid - side_b.get_center()) < 0:
            perp_b = -perp_b
        P_b1 = A + perp_b
        P_b2 = B + perp_b
        square_b = Polygon(A, B, P_b2, P_b1, color=GREEN, fill_opacity=0.3, stroke_width=2)

        # Square on side c (AC, outward)
        side_c_vec = C - A
        perp_c = np.array([-side_c_vec[1], side_c_vec[0], 0])
        if np.dot(perp_c, centroid - side_c.get_center()) < 0:
            perp_c = -perp_c
        P_c1 = A + perp_c
        P_c2 = C + perp_c
        square_c = Polygon(A, C, P_c2, P_c1, color=RED, fill_opacity=0.3, stroke_width=2)

        area_text = Text("Area = side²", font_size=30, color=WHITE)
        area_text.next_to(square_b.get_center(), DOWN, buff=0.3)

        self.play(ShowCreation(square_a), run_time=2)
        self.play(ShowCreation(square_b), run_time=2)
        self.play(ShowCreation(square_c), run_time=2)
        self.play(FadeIn(area_text, shift=UP * 0.3), run_time=0.8)
        self.wait(3.2)

        # Act 4: Area Intuition Before Formula (~10s)
        # Simplified grid representation (not full tiles for brevity)
        grid_a = VGroup(*[Line(square_a.get_corner(UL) + RIGHT * i * 0.2, square_a.get_corner(DL) + RIGHT * i * 0.2, color=BLUE, stroke_width=1) for i in range(1, 5)])
        grid_a.add(*[Line(square_a.get_corner(UL) + DOWN * i * 0.2, square_a.get_corner(UR) + DOWN * i * 0.2, color=BLUE, stroke_width=1) for i in range(1, 5)])
        grid_b = VGroup(*[Line(square_b.get_corner(UL) + RIGHT * i * 0.2, square_b.get_corner(UR) + RIGHT * i * 0.2, color=GREEN, stroke_width=1) for i in range(1, 5)])
        grid_b.add(*[Line(square_b.get_corner(UL) + DOWN * i * 0.2, square_b.get_corner(DL) + DOWN * i * 0.2, color=GREEN, stroke_width=1) for i in range(1, 5)])
        grid_c = VGroup(*[Line(square_c.get_corner(UL) + RIGHT * i * 0.2, square_c.get_corner(DL) + RIGHT * i * 0.2, color=RED, stroke_width=1) for i in range(1, 3)])
        grid_c.add(*[Line(square_c.get_corner(UL) + DOWN * i * 0.2, square_c.get_corner(UR) + DOWN * i * 0.2, color=RED, stroke_width=1) for i in range(1, 3)])

        self.play(FadeIn(grid_a), FadeIn(grid_b), run_time=2)
        self.wait(2)
        self.play(FadeIn(grid_c), run_time=1.5)
        self.wait(4.5)

        # Act 5: Statement of the Theorem (~8s)
        equation = Text("a² + b² = c²", font_size=40, color=WHITE)
        equation.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(equation, shift=UP * 0.3), run_time=0.8)
        self.play(Indicate(square_a, color=YELLOW), run_time=1)
        self.play(Indicate(square_b, color=YELLOW), run_time=1)
        self.play(Indicate(square_c, color=YELLOW), run_time=1)
        self.wait(4.2)

        # Act 6: Rearrangement Proof Setup (~12s)
        act1_objects = VGroup(grid, point1, point2, diagonal, question, side_a, side_b, side_c, right_angle_marker, label_a, label_b, label_c, square_a, square_b, square_c, area_text, grid_a, grid_b, grid_c, equation)
        self.play(FadeOut(act1_objects), run_time=1)
        self.wait(0.5)

        big_side = 4.0
        big_square = Square(side_length=big_side, color=WHITE, fill_opacity=0.2)
        big_square.move_to(ORIGIN)
        tri1 = Polygon([0, 0, 0], [2, 0, 0], [2, 2, 0], color=BLUE)
        tri2 = Polygon([0, 0, 0], [0, 2, 0], [2, 2, 0], color=BLUE)
        tri3 = Polygon([0, 2, 0], [2, 2, 0], [2, 4, 0], color=BLUE)
        tri4 = Polygon([2, 0, 0], [2, 2, 0], [4, 2, 0], color=BLUE)
        center_square = Square(side_length=2.0, color=RED, fill_opacity=0.3)
        center_square.rotate(PI/4)
        center_square.move_to([2, 2, 0])

        self.play(ShowCreation(big_square), run_time=2)
        self.play(ShowCreation(tri1), ShowCreation(tri2), ShowCreation(tri3), ShowCreation(tri4), run_time=3)
        self.play(ShowCreation(center_square), run_time=2)
        self.wait(5)

        # Act 7: Area Method 1 (~12s)
        area_expr1 = Text("Area = (a + b)² - 4(ab/2)", font_size=30, color=WHITE)
        area_expr1.to_edge(DOWN, buff=0.5)

        self.play(big_square.animate.set_fill(WHITE, opacity=0.5), run_time=1.5)
        self.play(Indicate(tri1), Indicate(tri2), Indicate(tri3), Indicate(tri4), run_time=2)
        self.play(tri1.animate.set_fill(opacity=0.1), tri2.animate.set_fill(opacity=0.1), tri3.animate.set_fill(opacity=0.1), tri4.animate.set_fill(opacity=0.1), run_time=1.5)
        self.play(FadeIn(area_expr1, shift=UP * 0.3), run_time=1)
        self.wait(6)

        # Act 8: Area Method 2 (~8s)
        area_expr2 = Text("Area = c²", font_size=30, color=RED)
        area_expr2.to_edge(DOWN, buff=0.5)

        self.play(big_square.animate.set_fill(opacity=0.1), tri1.animate.set_fill(opacity=0.05), tri2.animate.set_fill(opacity=0.05), tri3.animate.set_fill(opacity=0.05), tri4.animate.set_fill(opacity=0.05), run_time=1)
        self.play(center_square.animate.set_fill(RED, opacity=0.6), run_time=1.5)
        self.play(FadeTransform(area_expr1, area_expr2), run_time=0.8)
        self.wait(4.7)

        # Act 9: Equate and Simplify (~14s)
        step1 = Text("(a + b)² - 4(ab/2) = c²", font_size=30, color=WHITE)
        step2 = Text("a² + 2ab + b² - 2ab = c²", font_size=30, color=WHITE)
        step3 = Text("a² + b² = c²", font_size=30, color=WHITE)
        step1.to_edge(DOWN, buff=0.5)
        step2.to_edge(DOWN, buff=0.5)
        step3.to_edge(DOWN, buff=0.5)

        self.play(FadeTransform(area_expr2, step1), run_time=1)
        self.wait(3)
        self.play(FadeTransform(step1, step2), run_time=1.5)
        self.wait(3)
        self.play(FadeTransform(step2, step3), run_time=1.5)
        self.wait(4)

        # Act 10: Numeric Example (~10s)
        act2_objects = VGroup(big_square, tri1, tri2, tri3, tri4, center_square, step3)
        self.play(FadeOut(act2_objects), run_time=1)
        self.wait(0.5)

        A_num = np.array([-2, -1.5, 0])
        B_num = np.array([1, -1.5, 0])
        C_num = np.array([1, 1.5, 0])
        side_a_num = Line(B_num, C_num, color=BLUE)
        side_b_num = Line(A_num, B_num, color=GREEN)
        side_c_num = Line(A_num, C_num, color=RED)
        right_angle_num = Square(side_length=0.3, color=WHITE)
        right_angle_num.move_to(B_num)
        right_angle_num.align_to(B_num, DL)

        square_a_num = Polygon(B_num, C_num, C_num + np.array([0, 3, 0]), B_num + np.array([0, 3, 0]), color=BLUE, fill_opacity=0.3)
        square_b_num = Polygon(A_num, B_num, B_num + np.array([-3, 0, 0]), A_num + np.array([-3, 0, 0]), color=GREEN, fill_opacity=0.3)
        square_c_num = Polygon(A_num, C_num, C_num + np.array([-3, 0, 0]), A_num + np.array([0, 3, 0]), color=RED, fill_opacity=0.3)

        area_a = Integer(9, font_size=30, color=BLUE)
        area_b = Integer(16, font_size=30, color=GREEN)
        area_c = Integer(25, font_size=30, color=RED)
        area_a.move_to(square_a_num.get_center())
        area_b.move_to(square_b_num.get_center())
        area_c.move_to(square_c_num.get_center())
        label_c_num = Text("5", font_size=30, color=RED)
        label_c_num.next_to(side_c_num.get_center(), UL, buff=0.2)

        self.play(ShowCreation(side_a_num), ShowCreation(side_b_num), ShowCreation(side_c_num), ShowCreation(right_angle_num), run_time=1.5)
        self.play(ShowCreation(square_a_num), ShowCreation(square_b_num), ShowCreation(square_c_num), run_time=2)
        self.play(ChangeDecimalToValue(area_a, 9), ChangeDecimalToValue(area_b, 16), run_time=2)
        self.play(ChangeDecimalToValue(area_c, 25), FadeIn(label_c_num), run_time=2)
        self.wait(1.5)

        # Act 11: Coordinate Geometry Link (~12s)
        axes = Axes(x_range=(-5, 5, 1), y_range=(-3, 3, 1), width=10, height=6)
        axes.shift(0.5 * DOWN)
        axes.add_coordinate_labels(font_size=18)
        x_tracker = ValueTracker(2)
        y_tracker = ValueTracker(1)
        tri_coord = VGroup(
            Line(axes.c2p(0, 0), axes.c2p(x_tracker.get_value(), 0), color=GREEN),
            Line(axes.c2p(x_tracker.get_value(), 0), axes.c2p(x_tracker.get_value(), y_tracker.get_value()), color=BLUE),
            Line(axes.c2p(0, 0), axes.c2p(x_tracker.get_value(), y_tracker.get_value()), color=RED)
        )
        tri_coord.add_updater(lambda t: t.become(VGroup(
            Line(axes.c2p(0, 0), axes.c2p(x_tracker.get_value(), 0), color=GREEN),
            Line(axes.c2p(x_tracker.get_value(), 0), axes.c2p(x_tracker.get_value(), y_tracker.get_value()), color=BLUE),
            Line(axes.c2p(0, 0), axes.c2p(x_tracker.get_value(), y_tracker.get_value()), color=RED)
        )))
        dist_formula = Text("distance = √(x² + y²)", font_size=30, color=WHITE)
        dist_formula.to_edge(DOWN, buff=0.5)

        act3_objects = VGroup(side_a_num, side_b_num, side_c_num, right_angle_num, square_a_num, square_b_num, square_c_num, area_a, area_b, area_c, label_c_num)
        self.play(FadeOut(act3_objects), run_time=1)
        self.play(ShowCreation(axes), run_time=1.5)
        self.play(ShowCreation(tri_coord), run_time=1.5)
        self.play(x_tracker.animate.set_value(3), y_tracker.animate.set_value(2), run_time=2)
        self.play(x_tracker.animate.set_value(1), y_tracker.animate.set_value(2.5), run_time=2)
        self.play(FadeIn(dist_formula, shift=UP * 0.3), run_time=1)
        self.wait(2.5)
        tri_coord.clear_updaters()

        # Act 12: Continuous Deformation Insight (~10s)
        self.play(FadeOut(axes), FadeOut(dist_formula), run_time=1)
        A_def = np.array([-2, -1.5, 0])
        B_def = np.array([1, -1.5, 0])
        y_def_tracker = ValueTracker(1.5)
        C_def = np.array([1, y_def_tracker.get_value(), 0])
        side_a_def = Line(B_def, C_def, color=BLUE)
        side_b_def = Line(A_def, B_def, color=GREEN)
        side_c_def = Line(A_def, C_def, color=RED)
        side_a_def.add_updater(lambda l: l.become(Line(B_def, np.array([1, y_def_tracker.get_value(), 0]), color=BLUE)))
        side_c_def.add_updater(lambda l: l.become(Line(A_def, np.array([1, y_def_tracker.get_value(), 0]), color=RED)))
        square_a_def = always_redraw(lambda: Polygon(B_def, np.array([1, y_def_tracker.get_value(), 0]), np.array([1, y_def_tracker.get_value() + 3, 0]), B_def + np.array([0, 3, 0]), color=BLUE, fill_opacity=0.3))
        square_b_def = Polygon(A_def, B_def, B_def + np.array([-3, 0, 0]), A_def + np.array([-3, 0, 0]), color=GREEN, fill_opacity=0.3)
        square_c_def = always_redraw(lambda: Polygon(A_def, np.array([1, y_def_tracker.get_value(), 0]), np.array([1, y_def_tracker.get_value() - 3, 0]), A_def + np.array([0, -3, 0]), color=RED, fill_opacity=0.3))

        self.play(ShowCreation(side_a_def), ShowCreation(side_b_def), ShowCreation(side_c_def), run_time=1.5)
        self.play(ShowCreation(square_a_def), ShowCreation(square_b_def), ShowCreation(square_c_def), run_time=2)
        self.play(y_def_tracker.animate.set_value(0.5), run_time=2)
        self.play(y_def_tracker.animate.set_value(2.5), run_time=2)
        self.wait(1.5)
        side_a_def.clear_updaters()
        side_c_def.clear_updaters()

        # Act 13: 3D Teaser Extension (~10s)
        act4_objects = VGroup(side_a_def, side_b_def, side_c_def, square_a_def, square_b_def, square_c_def)
        self.play(FadeOut(act4_objects), run_time=1)
        box = VGroup(
            Line([-2, -1.5, 0], [2, -1.5, 0], color=GREEN),
            Line([2, -1.5, 0], [2, 1.5, 0], color=BLUE),
            Line([-2, -1.5, 0], [-2, 1.5, 0], color=BLUE),
            Line([-2, 1.5, 0], [2, 1.5, 0], color=GREEN),
            Line([-2, -1.5, 0], [-2, -1.5, 2], color=YELLOW),
            Line([2, -1.5, 0], [2, -1.5, 2], color=YELLOW),
            Line([-2, 1.5, 0], [-2, 1.5, 2], color=YELLOW),
            Line([2, 1.5, 0], [2, 1.5, 2], color=YELLOW),
            Line([-2, -1.5, 2], [2, -1.5, 2], color=GREEN),
            Line([2, -1.5, 2], [2, 1.5, 2], color=BLUE),
            Line([-2, -1.5, 2], [-2, 1.5, 2], color=BLUE),
            Line([-2, 1.5, 2], [2, 1.5, 2], color=GREEN)
        )
        face_diagonal = Line([-2, -1.5, 0], [2, 1.5, 0], color=RED)
        space_diagonal = Line([-2, -1.5, 0], [2, 1.5, 2], color=PURPLE)
        formula_3d = Text("a² + b² + d² = diagonal²", font_size=30, color=WHITE)
        formula_3d.to_edge(DOWN, buff=0.5)

        self.play(ShowCreation(box), run_time=2)
        self.play(ShowCreation(face_diagonal), run_time=1.5)
        self.play(ShowCreation(space_diagonal), run_time=1.5)
        self.play(FadeIn(formula_3d, shift=UP * 0.3), run_time=1)
        self.wait(3.5)

        # Act 14: Summary Frame (~8s)
        act5_objects = VGroup(box, face_diagonal, space_diagonal, formula_3d)
        self.play(FadeOut(act5_objects), run_time=1)
        A_final = np.array([-2, -1.5, 0])
        B_final = np.array([1, -1.5, 0])
        C_final = np.array([1, 1.5, 0])
        side_a_final = Line(B_final, C_final, color=BLUE)
        side_b_final = Line(A_final, B_final, color=GREEN)
        side_c_final = Line(A_final, C_final, color=RED)
        right_angle_final = Square(side_length=0.3, color=WHITE)
        right_angle_final.move_to(B_final)
        right_angle_final.align_to(B_final, DL)
        square_a_final = Polygon(B_final, C_final, C_final + np.array([0, 3, 0]), B_final + np.array([0, 3, 0]), color=BLUE, fill_opacity=0.3)
        square_b_final = Polygon(A_final, B_final, B_final + np.array([-3, 0, 0]), A_final + np.array([-3, 0, 0]), color=GREEN, fill_opacity=0.3)
        square_c_final = Polygon(A_final, C_final, C_final + np.array([-3, 0, 0]), A_final + np.array([0, 3, 0]), color=RED, fill_opacity=0.3)
        final_eq = Text("a² + b² = c²", font_size=40, color=WHITE)
        final_eq.to_edge(DOWN, buff=0.5)

        self.play(ShowCreation(side_a_final), ShowCreation(side_b_final), ShowCreation(side_c_final), ShowCreation(right_angle_final), run_time=1.5)
        self.play(ShowCreation(square_a_final), ShowCreation(square_b_final), ShowCreation(square_c_final), run_time=2)
        self.play(FadeIn(final_eq, shift=UP * 0.3), run_time=1)
        self.play(Indicate(square_a_final, color=YELLOW), Indicate(square_b_final, color=YELLOW), Indicate(square_c_final, color=YELLOW), run_time=2)
        self.wait(1.5)
        self.play(FadeOut(VGroup(side_a_final, side_b_final, side_c_final, right_angle_final, square_a_final, square_b_final, square_c_final, final_eq)), run_time=1)