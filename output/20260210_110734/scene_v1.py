from manimlib import *

class GeneratedScene(Scene):
    def construct(self):
        # ── Act 1: Introduction & Unit Square (~10s) ─────────────────────────
        title = Text("Linear Transformations", font_size=60)
        self.play(FadeIn(title, scale=0.8), run_time=1)
        self.wait(1.5)
        self.play(title.animate.scale(0.5).to_edge(UP), run_time=0.8)

        square = Square(side_length=2, color=BLUE)
        square.move_to(ORIGIN)
        i_vec = Vector(RIGHT * 1, color=RED)
        j_vec = Vector(UP * 1, color=GREEN)
        i_label = Text("i", font_size=24, color=RED).next_to(i_vec.get_end(), RIGHT, buff=0.1)
        j_label = Text("j", font_size=24, color=GREEN).next_to(j_vec.get_end(), UP, buff=0.1)

        self.play(ShowCreation(square), run_time=1.5)
        self.play(GrowArrow(i_vec), GrowArrow(j_vec), FadeIn(i_label), FadeIn(j_label), run_time=1.5)
        self.wait(1.5)

        # ── Act 2: Scaling Transformation (~15s) ─────────────────────────
        grid = NumberPlane(x_range=(-5, 5), y_range=(-3, 3), width=10, height=6)
        grid.shift(0.5 * DOWN)
        grid.prepare_for_nonlinear_transform()

        scaling_matrix = [[2, 0], [0, 0.5]]
        scaled_square = square.copy().apply_matrix(scaling_matrix)
        scaled_i_vec = i_vec.copy().apply_matrix(scaling_matrix)
        scaled_j_vec = j_vec.copy().apply_matrix(scaling_matrix)
        scaled_i_label = Text("i'", font_size=24, color=RED).next_to(scaled_i_vec.get_end(), RIGHT, buff=0.1)
        scaled_j_label = Text("j'", font_size=24, color=GREEN).next_to(scaled_j_vec.get_end(), UP, buff=0.1)

        matrix_label_scale = Text("Matrix: [[2, 0], [0, 0.5]]", font_size=24, color=WHITE)
        matrix_label_scale.to_corner(UR, buff=0.5)

        self.play(FadeIn(grid, run_time=1))
        self.play(
            Transform(square, scaled_square),
            Transform(i_vec, scaled_i_vec),
            Transform(j_vec, scaled_j_vec),
            FadeTransform(i_label, scaled_i_label),
            FadeTransform(j_label, scaled_j_label),
            grid.animate.apply_matrix(scaling_matrix),
            run_time=2
        )
        self.play(FadeIn(matrix_label_scale, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)

        # ── Act 3: Rotation Transformation (~15s) ─────────────────────────
        act2_objects = VGroup(square, i_vec, j_vec, scaled_i_label, scaled_j_label, matrix_label_scale)
        self.play(FadeOut(act2_objects), run_time=1)
        self.wait(0.5)

        square = Square(side_length=2, color=BLUE).move_to(ORIGIN)
        i_vec = Vector(RIGHT * 1, color=RED)
        j_vec = Vector(UP * 1, color=GREEN)
        i_label = Text("i", font_size=24, color=RED).next_to(i_vec.get_end(), RIGHT, buff=0.1)
        j_label = Text("j", font_size=24, color=GREEN).next_to(j_vec.get_end(), UP, buff=0.1)

        angle = PI / 4  # 45 degrees
        rotation_matrix = [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
        rotated_square = square.copy().apply_matrix(rotation_matrix)
        rotated_i_vec = i_vec.copy().apply_matrix(rotation_matrix)
        rotated_j_vec = j_vec.copy().apply_matrix(rotation_matrix)
        rotated_i_label = Text("i'", font_size=24, color=RED).next_to(rotated_i_vec.get_end(), UR, buff=0.1)
        rotated_j_label = Text("j'", font_size=24, color=GREEN).next_to(rotated_j_vec.get_end(), UR, buff=0.1)

        matrix_label_rot = Text("Matrix: [[cos(45°), -sin(45°)], [sin(45°), cos(45°)]]", font_size=24, color=WHITE)
        matrix_label_rot.to_corner(UR, buff=0.5)

        grid.prepare_for_nonlinear_transform()
        self.play(ShowCreation(square), GrowArrow(i_vec), GrowArrow(j_vec), FadeIn(i_label), FadeIn(j_label), run_time=1.5)
        self.play(
            Transform(square, rotated_square),
            Transform(i_vec, rotated_i_vec),
            Transform(j_vec, rotated_j_vec),
            FadeTransform(i_label, rotated_i_label),
            FadeTransform(j_label, rotated_j_label),
            grid.animate.apply_matrix(rotation_matrix),
            run_time=2
        )
        self.play(FadeIn(matrix_label_rot, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)

        # ── Act 4: Shear Transformation (~15s) ─────────────────────────
        act3_objects = VGroup(square, i_vec, j_vec, rotated_i_label, rotated_j_label, matrix_label_rot)
        self.play(FadeOut(act3_objects), run_time=1)
        self.wait(0.5)

        square = Square(side_length=2, color=BLUE).move_to(ORIGIN)
        i_vec = Vector(RIGHT * 1, color=RED)
        j_vec = Vector(UP * 1, color=GREEN)
        i_label = Text("i", font_size=24, color=RED).next_to(i_vec.get_end(), RIGHT, buff=0.1)
        j_label = Text("j", font_size=24, color=GREEN).next_to(j_vec.get_end(), UP, buff=0.1)

        shear_matrix = [[1, 1], [0, 1]]
        sheared_square = square.copy().apply_matrix(shear_matrix)
        sheared_i_vec = i_vec.copy().apply_matrix(shear_matrix)
        sheared_j_vec = j_vec.copy().apply_matrix(shear_matrix)
        sheared_i_label = Text("i'", font_size=24, color=RED).next_to(sheared_i_vec.get_end(), UR, buff=0.1)
        sheared_j_label = Text("j'", font_size=24, color=GREEN).next_to(sheared_j_vec.get_end(), UP, buff=0.1)

        matrix_label_shear = Text("Matrix: [[1, 1], [0, 1]]", font_size=24, color=WHITE)
        matrix_label_shear.to_corner(UR, buff=0.5)

        grid.prepare_for_nonlinear_transform()
        self.play(ShowCreation(square), GrowArrow(i_vec), GrowArrow(j_vec), FadeIn(i_label), FadeIn(j_label), run_time=1.5)
        self.play(
            Transform(square, sheared_square),
            Transform(i_vec, sheared_i_vec),
            Transform(j_vec, sheared_j_vec),
            FadeTransform(i_label, sheared_i_label),
            FadeTransform(j_label, sheared_j_label),
            grid.animate.apply_matrix(shear_matrix),
            run_time=2
        )
        self.play(FadeIn(matrix_label_shear, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)

        # ── Act 5: Reflection Transformation (~15s) ─────────────────────────
        act4_objects = VGroup(square, i_vec, j_vec, sheared_i_label, sheared_j_label, matrix_label_shear)
        self.play(FadeOut(act4_objects), run_time=1)
        self.wait(0.5)

        square = Square(side_length=2, color=BLUE).move_to(ORIGIN)
        i_vec = Vector(RIGHT * 1, color=RED)
        j_vec = Vector(UP * 1, color=GREEN)
        i_label = Text("i", font_size=24, color=RED).next_to(i_vec.get_end(), RIGHT, buff=0.1)
        j_label = Text("j", font_size=24, color=GREEN).next_to(j_vec.get_end(), UP, buff=0.1)

        reflection_matrix = [[-1, 0], [0, 1]]
        reflected_square = square.copy().apply_matrix(reflection_matrix)
        reflected_i_vec = i_vec.copy().apply_matrix(reflection_matrix)
        reflected_j_vec = j_vec.copy().apply_matrix(reflection_matrix)
        reflected_i_label = Text("i'", font_size=24, color=RED).next_to(reflected_i_vec.get_end(), LEFT, buff=0.1)
        reflected_j_label = Text("j'", font_size=24, color=GREEN).next_to(reflected_j_vec.get_end(), UP, buff=0.1)

        matrix_label_reflect = Text("Matrix: [[-1, 0], [0, 1]]", font_size=24, color=WHITE)
        matrix_label_reflect.to_corner(UR, buff=0.5)

        grid.prepare_for_nonlinear_transform()
        self.play(ShowCreation(square), GrowArrow(i_vec), GrowArrow(j_vec), FadeIn(i_label), FadeIn(j_label), run_time=1.5)
        self.play(
            Transform(square, reflected_square),
            Transform(i_vec, reflected_i_vec),
            Transform(j_vec, reflected_j_vec),
            FadeTransform(i_label, reflected_i_label),
            FadeTransform(j_label, reflected_j_label),
            grid.animate.apply_matrix(reflection_matrix),
            run_time=2
        )
        self.play(FadeIn(matrix_label_reflect, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)

        # ── Act 6: Matrix Composition (~15s) ─────────────────────────
        act5_objects = VGroup(square, i_vec, j_vec, reflected_i_label, reflected_j_label, matrix_label_reflect)
        self.play(FadeOut(act5_objects), run_time=1)
        self.wait(0.5)

        square = Square(side_length=2, color=BLUE).move_to(ORIGIN)
        scaling_matrix = [[2, 0], [0, 0.5]]
        rotation_matrix = [[np.cos(PI/4), -np.sin(PI/4)], [np.sin(PI/4), np.cos(PI/4)]]
        scaled_square = square.copy().apply_matrix(scaling_matrix)
        final_square = square.copy().apply_matrix(np.dot(rotation_matrix, scaling_matrix))

        matrix_label_comp1 = Text("Scale: [[2, 0], [0, 0.5]]", font_size=24, color=WHITE)
        matrix_label_comp2 = Text("Rotate: [[cos(45°), -sin(45°)], [sin(45°), cos(45°)]]", font_size=24, color=WHITE)
        matrix_label_comp3 = Text("Product: Scale then Rotate", font_size=24, color=WHITE)
        comp_group = VGroup(matrix_label_comp1, matrix_label_comp2, matrix_label_comp3).arrange(DOWN, buff=0.3)
        comp_group.to_corner(UR, buff=0.5)

        grid.prepare_for_nonlinear_transform()
        self.play(ShowCreation(square), run_time=1)
        self.play(FadeIn(matrix_label_comp1), run_time=0.5)
        self.play(Transform(square, scaled_square), grid.animate.apply_matrix(scaling_matrix), run_time=1.5)
        self.play(FadeIn(matrix_label_comp2), run_time=0.5)
        self.play(Transform(square, final_square), grid.animate.apply_matrix(np.dot(rotation_matrix, scaling_matrix)), run_time=1.5)
        self.play(FadeIn(matrix_label_comp3), run_time=0.5)
        self.wait(1.5)

        # ── Act 7: Determinant as Area Scaling (~10s) ─────────────────────────
        act6_objects = VGroup(square, comp_group)
        self.play(FadeOut(act6_objects), run_time=1)
        self.wait(0.5)

        square = Square(side_length=2, color=BLUE).move_to(ORIGIN)
        area_label = Text("Area = 1", font_size=24, color=BLUE).next_to(square, DOWN, buff=0.2)
        scaling_matrix = [[2, 0], [0, 0.5]]
        scaled_square = square.copy().apply_matrix(scaling_matrix)
        area_label_new = Text("Area = 2 × 0.5 = 1", font_size=24, color=BLUE).next_to(scaled_square, DOWN, buff=0.2)
        det_label = Text("Determinant = 1", font_size=24, color=WHITE).to_corner(UR, buff=0.5)

        grid.prepare_for_nonlinear_transform()
        self.play(ShowCreation(square), FadeIn(area_label), run_time=1.5)
        self.play(
            Transform(square, scaled_square),
            FadeTransform(area_label, area_label_new),
            grid.animate.apply_matrix(scaling_matrix),
            run_time=1.5
        )
        self.play(FadeIn(det_label), run_time=0.8)
        self.wait(1.5)

        # ── Act 8: Eigenvectors as Invariant Directions (~15s) ─────────────────────────
        act7_objects = VGroup(square, area_label_new, det_label)
        self.play(FadeOut(act7_objects), run_time=1)
        self.wait(0.5)

        square = Square(side_length=2, color=BLUE).move_to(ORIGIN)
        scaling_matrix = [[2, 0], [0, 0.5]]
        scaled_square = square.copy().apply_matrix(scaling_matrix)
        eig_vec1 = Vector(RIGHT * 2, color=YELLOW)
        eig_vec2 = Vector(UP * 1, color=YELLOW)
        eig_label1 = Text("Eigenvector", font_size=24, color=YELLOW).next_to(eig_vec1.get_end(), RIGHT, buff=0.2)
        eig_label2 = Text("Eigenvector", font_size=24, color=YELLOW).next_to(eig_vec2.get_end(), UP, buff=0.2)

        grid.prepare_for_nonlinear_transform()
        self.play(ShowCreation(square), run_time=1)
        self.play(Transform(square, scaled_square), grid.animate.apply_matrix(scaling_matrix), run_time=1.5)
        self.play(GrowArrow(eig_vec1), GrowArrow(eig_vec2), run_time=1.5)
        self.play(FadeIn(eig_label1), FadeIn(eig_label2), run_time=0.8)
        self.wait(1.5)

        # ── Closing (~5s) ────────────────────────────────────────
        all_objs = VGroup(title, square, eig_vec1, eig_vec2, eig_label1, eig_label2, grid)
        closing = Text(
            "Linear transformations reshape space\nvia matrices, with composition,\narea scaling, and invariant directions",
            font_size=36
        )

        self.play(FadeOut(all_objs), run_time=1)
        self.play(FadeIn(closing, scale=0.9), run_time=1)
        self.wait(2)
        self.play(FadeOut(closing), run_time=1)