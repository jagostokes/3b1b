from manimlib import *

class GeneratedScene(Scene):
    def construct(self):
        # ACT 1: Introduction
        title = Text("Linear Transformations", font_size=60)
        self.play(FadeIn(title, scale=0.8), run_time=1)
        self.wait(0.5)
        self.play(title.animate.scale(0.5).to_edge(UP), run_time=0.8)

        unit_square = Square(side_length=2, color=WHITE)
        unit_square.move_to(ORIGIN)
        i_vec = Arrow(ORIGIN, RIGHT * 2, color=RED, buff=0)
        j_vec = Arrow(ORIGIN, UP * 2, color=GREEN, buff=0)
        basis_label_i = Text("i", font_size=24, color=RED).next_to(i_vec.get_end(), RIGHT, buff=0.1)
        basis_label_j = Text("j", font_size=24, color=GREEN).next_to(j_vec.get_end(), UP, buff=0.1)

        self.play(ShowCreation(unit_square), run_time=1)
        self.play(GrowArrow(i_vec), GrowArrow(j_vec), FadeIn(basis_label_i), FadeIn(basis_label_j), run_time=1.5)
        self.wait(1)

        # ACT 2: Basis Vector Transformations (Scaling)
        matrix_text = Text("Matrix: [[2, 0], [0, 1]]", font_size=30).to_edge(DOWN)
        self.play(FadeIn(matrix_text), run_time=0.5)
        new_i_vec = Arrow(ORIGIN, RIGHT * 4, color=RED, buff=0)
        new_i_label = Text("2i", font_size=24, color=RED).next_to(new_i_vec.get_end(), RIGHT, buff=0.1)
        new_square = Rectangle(width=4, height=2, color=WHITE).move_to(ORIGIN)

        self.play(Transform(i_vec, new_i_vec), Transform(basis_label_i, new_i_label), run_time=1.5)
        self.play(Transform(unit_square, new_square), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(VGroup(unit_square, i_vec, j_vec, basis_label_i, basis_label_j, matrix_text, new_i_vec, new_i_label, new_square)), run_time=1)

        # ACT 3: Grid Deformation for Different Transformations
        grid = NumberPlane(x_range=(-5, 5, 1), y_range=(-5, 5, 1), width=10, height=10)
        self.play(ShowCreation(grid), run_time=1)

        scaling_label = Text("Scaling", font_size=30).to_edge(DOWN)
        self.play(FadeIn(scaling_label), run_time=0.5)
        self.play(grid.animate.apply_matrix([[2, 0], [0, 1]]), run_time=2)
        self.wait(0.5)

        rotation_label = Text("Rotation (90°)", font_size=30).to_edge(DOWN)
        self.play(FadeTransform(scaling_label, rotation_label), run_time=0.5)
        self.play(grid.animate.apply_matrix([[0, -1], [1, 0]]), run_time=2)
        self.wait(0.5)

        shear_label = Text("Shear", font_size=30).to_edge(DOWN)
        self.play(FadeTransform(rotation_label, shear_label), run_time=0.5)
        self.play(grid.animate.apply_matrix([[1, 1], [0, 1]]), run_time=2)
        self.wait(0.5)

        reflection_label = Text("Reflection (y-axis)", font_size=30).to_edge(DOWN)
        self.play(FadeTransform(shear_label, reflection_label), run_time=0.5)
        self.play(grid.animate.apply_matrix([[-1, 0], [0, 1]]), run_time=2)
        self.wait(0.5)
        self.play(FadeOut(grid), FadeOut(reflection_label), run_time=1)

        # ACT 4: Matrix Multiplication as Composition
        grid2 = NumberPlane(x_range=(-5, 5, 1), y_range=(-5, 5, 1), width=10, height=10)
        self.play(ShowCreation(grid2), run_time=1)
        comp_label = Text("Composition: Rotation then Shear", font_size=30).to_edge(DOWN)
        self.play(FadeIn(comp_label), run_time=0.5)
        self.play(grid2.animate.apply_matrix([[0, -1], [1, 0]]), run_time=2)
        self.play(grid2.animate.apply_matrix([[1, 1], [0, 1]]), run_time=2)
        self.wait(0.5)
        self.play(FadeOut(grid2), FadeOut(comp_label), run_time=1)

        # ACT 5: Determinant as Area Scaling
        unit_square2 = Square(side_length=2, color=WHITE, fill_opacity=0.3)
        unit_square2.move_to(ORIGIN)
        area_label1 = Text("Area = 1", font_size=30).to_edge(DOWN)
        self.play(ShowCreation(unit_square2), FadeIn(area_label1), run_time=1)
        transformed_square = Rectangle(width=4, height=2, color=WHITE, fill_opacity=0.3).move_to(ORIGIN)
        area_label2 = Text("Area = 2 (Determinant)", font_size=30).to_edge(DOWN)
        self.play(Transform(unit_square2, transformed_square), FadeTransform(area_label1, area_label2), run_time=2)
        self.wait(1)
        self.play(FadeOut(unit_square2), FadeOut(area_label2), run_time=1)

        # ACT 6: Eigenvectors as Invariant Directions
        matrix_eigen = Text("Matrix: [[2, 0], [0, 1]]", font_size=30).to_edge(DOWN)
        eigen_vec1 = Arrow(ORIGIN, RIGHT * 2, color=RED, buff=0)
        eigen_vec2 = Arrow(ORIGIN, UP * 2, color=GREEN, buff=0)
        eigen_label = Text("Eigenvectors: Invariant Directions", font_size=30).next_to(title, DOWN)
        self.play(FadeIn(matrix_eigen), GrowArrow(eigen_vec1), GrowArrow(eigen_vec2), FadeIn(eigen_label), run_time=1.5)
        new_eigen_vec1 = Arrow(ORIGIN, RIGHT * 4, color=RED, buff=0)
        new_eigen_vec2 = Arrow(ORIGIN, UP * 2, color=GREEN, buff=0)
        self.play(Transform(eigen_vec1, new_eigen_vec1), Transform(eigen_vec2, new_eigen_vec2), run_time=2)
        self.wait(1)

        # CLOSING
        final_text = Text("Linear Transformations", font_size=60)
        self.play(FadeOut(VGroup(eigen_vec1, eigen_vec2, new_eigen_vec1, new_eigen_vec2, matrix_eigen, eigen_label, title)), FadeIn(final_text), run_time=1)
        self.wait(1)
        self.play(FadeOut(final_text), run_time=1)