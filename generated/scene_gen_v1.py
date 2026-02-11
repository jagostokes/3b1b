from manimlib import *

class GeneratedScene(Scene):
    def construct(self):
        # Act 1: Introduction to Linear Transformations
        title = Text("Linear Transformations as Space Movers", font_size=50)
        unit_square = Square(side_length=2, color=WHITE, fill_opacity=0.2)
        unit_square.set_fill(WHITE, opacity=0.2)
        basis_i = Arrow(ORIGIN, RIGHT * 2, color=RED, buff=0)
        basis_j = Arrow(ORIGIN, UP * 2, color=BLUE, buff=0)
        label_i = Text("i", font_size=24, color=RED).next_to(basis_i.get_end(), RIGHT, buff=0.1)
        label_j = Text("j", font_size=24, color=BLUE).next_to(basis_j.get_end(), UP, buff=0.1)
        desc = Text("Unit Square and Basis Vectors", font_size=30).shift(DOWN * 3)

        self.play(FadeIn(title, scale=0.8), run_time=1)
        self.play(ShowCreation(unit_square), run_time=1)
        self.play(ShowCreation(basis_i), FadeIn(label_i), run_time=1)
        self.play(ShowCreation(basis_j), FadeIn(label_j), run_time=1)
        self.play(FadeIn(desc, shift=UP * 0.3), run_time=0.8)
        self.wait(1)

        # Act 2: Transforming the Unit Square
        scaling_title = Text("Scaling Matrix", font_size=50)
        matrix_text = Text("[[2, 0], [0, 1]]", font_size=30)
        matrix_text.next_to(scaling_title, DOWN, buff=0.5)

        self.play(FadeOut(title), FadeIn(scaling_title, scale=0.8), run_time=1)
        self.play(FadeIn(matrix_text, shift=UP * 0.3), run_time=0.8)
        self.play(
            ApplyMatrix([[2, 0], [0, 1]], unit_square),
            ApplyMatrix([[2, 0], [0, 1]], basis_i),
            ApplyMatrix([[2, 0], [0, 1]], basis_j),
            ApplyMatrix([[2, 0], [0, 1]], label_i),
            ApplyMatrix([[2, 0], [0, 1]], label_j),
            run_time=2
        )
        self.wait(1)

        # Act 3: Grid Deformations for Different Transformations
        grid = VGroup(*[
            Square(side_length=1, color=WHITE, fill_opacity=0.1).shift(RIGHT * i + UP * j)
            for i in range(-2, 3) for j in range(-2, 3)
        ])
        rotation_title = Text("Rotation", font_size=50)
        shear_title = Text("Shear", font_size=50)
        reflection_title = Text("Reflection", font_size=50)
        matrix_rot = Text("[[0, -1], [1, 0]]", font_size=30).next_to(rotation_title, DOWN, buff=0.5)
        matrix_shear = Text("[[1, 1], [0, 1]]", font_size=30).next_to(shear_title, DOWN, buff=0.5)
        matrix_refl = Text("[[1, 0], [0, -1]]", font_size=30).next_to(reflection_title, DOWN, buff=0.5)

        self.play(FadeOut(VGroup(unit_square, basis_i, basis_j, label_i, label_j, scaling_title, matrix_text)), run_time=1)
        self.play(ShowCreation(grid), run_time=1.5)
        self.play(FadeIn(rotation_title, scale=0.8), FadeIn(matrix_rot, shift=UP * 0.3), run_time=0.8)
        self.play(ApplyMatrix([[0, -1], [1, 0]], grid), run_time=2)
        self.play(FadeOut(rotation_title), FadeOut(matrix_rot), FadeIn(shear_title, scale=0.8), FadeIn(matrix_shear, shift=UP * 0.3), run_time=1)
        self.play(ApplyMatrix([[1, 1], [0, 1]], grid), run_time=2)
        self.play(FadeOut(shear_title), FadeOut(matrix_shear), FadeIn(reflection_title, scale=0.8), FadeIn(matrix_refl, shift=UP * 0.3), run_time=1)
        self.play(ApplyMatrix([[1, 0], [0, -1]], grid), run_time=2)
        self.wait(1)

        # Act 4: Points Follow Basis Vectors
        point_follow_title = Text("Points Follow Basis", font_size=50)
        original_square = Square(side_length=2, color=WHITE, fill_opacity=0.2)
        original_i = Arrow(ORIGIN, RIGHT * 2, color=RED, buff=0)
        original_j = Arrow(ORIGIN, UP * 2, color=BLUE, buff=0)
        label_i2 = Text("i", font_size=24, color=RED).next_to(original_i.get_end(), RIGHT, buff=0.1)
        label_j2 = Text("j", font_size=24, color=BLUE).next_to(original_j.get_end(), UP, buff=0.1)
        point = Dot(ORIGIN + RIGHT + UP, color=YELLOW)
        path = Line(ORIGIN + RIGHT + UP, ORIGIN + RIGHT * 2 + UP, color=YELLOW)

        self.play(FadeOut(VGroup(grid, reflection_title, matrix_refl)), run_time=1)
        self.play(ShowCreation(original_square), ShowCreation(original_i), ShowCreation(original_j), FadeIn(label_i2), FadeIn(label_j2), run_time=1.5)
        self.play(FadeIn(point_follow_title, scale=0.8), run_time=0.8)
        self.play(FadeIn(point, scale=0.8), run_time=0.8)
        self.play(
            ApplyMatrix([[2, 0], [0, 1]], original_square),
            ApplyMatrix([[2, 0], [0, 1]], original_i),
            ApplyMatrix([[2, 0], [0, 1]], original_j),
            ApplyMatrix([[2, 0], [0, 1]], label_i2),
            ApplyMatrix([[2, 0], [0, 1]], label_j2),
            ApplyMatrix([[2, 0], [0, 1]], point),
            run_time=2
        )
        self.play(ShowCreation(path), run_time=1)
        self.wait(1)

        # Act 5: Matrix Multiplication as Composition
        comp_title = Text("Composition of Transformations", font_size=50)
        matrix1 = Text("[[2, 0], [0, 1]]", font_size=30).shift(LEFT * 3)
        matrix2 = Text("[[0, -1], [1, 0]]", font_size=30).next_to(matrix1, RIGHT, buff=1)
        matrix_result = Text("[[0, -2], [1, 0]]", font_size=30).next_to(matrix2, RIGHT, buff=1)
        unit_square2 = Square(side_length=2, color=WHITE, fill_opacity=0.2)

        self.play(FadeOut(VGroup(original_square, original_i, original_j, label_i2, label_j2, point, path, point_follow_title, desc)), run_time=1)
        self.play(FadeIn(comp_title, scale=0.8), run_time=0.8)
        self.play(ShowCreation(unit_square2), run_time=1)
        self.play(FadeIn(matrix1, shift=UP * 0.3), run_time=0.8)
        self.play(ApplyMatrix([[2, 0], [0, 1]], unit_square2), run_time=2)
        self.play(FadeIn(matrix2, shift=UP * 0.3), run_time=0.8)
        self.play(ApplyMatrix([[0, -1], [1, 0]], unit_square2), run_time=2)
        self.play(FadeIn(matrix_result, shift=UP * 0.3), run_time=0.8)
        self.wait(1)

        # Act 6: Determinants and Area Scaling
        det_title = Text("Determinants Scale Area", font_size=50)
        area_label = Text("Area = 1", font_size=30).shift(DOWN * 3)
        scaled_area_label = Text("Area = 2", font_size=30).shift(DOWN * 3)
        unit_square_copy = Square(side_length=2, color=WHITE, fill_opacity=0.2)

        self.play(FadeOut(VGroup(comp_title, matrix1, matrix2, matrix_result, unit_square2)), run_time=1)
        self.play(FadeIn(det_title, scale=0.8), run_time=0.8)
        self.play(ShowCreation(unit_square_copy), FadeIn(area_label, shift=UP * 0.3), run_time=1.5)
        self.play(ApplyMatrix([[2, 0], [0, 1]], unit_square_copy), run_time=2)
        self.play(FadeOut(area_label), FadeIn(scaled_area_label, shift=UP * 0.3), run_time=0.8)
        self.wait(1)

        # Closing: Eigenvectors
        eigen_title = Text("Eigenvectors: Invariant Directions", font_size=50)
        eigen_vector = Arrow(ORIGIN, RIGHT * 2 + UP * 2, color=GREEN, buff=0)

        self.play(FadeOut(VGroup(det_title, unit_square_copy, scaled_area_label)), run_time=1)
        self.play(FadeIn(eigen_title, scale=0.8), run_time=0.8)
        self.play(ShowCreation(eigen_vector), run_time=1.5)
        self.play(ApplyMatrix([[2, 0], [0, 2]], eigen_vector), run_time=2)
        self.wait(1)
        self.play(FadeOut(VGroup(eigen_title, eigen_vector)), run_time=1.5)