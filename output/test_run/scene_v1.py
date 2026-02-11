from manimlib import *

class GeneratedScene(Scene):
    def construct(self):
        # Act 1: Introduction to Linear Transformations
        title = Text("Linear Transformations as Space Movers", font_size=50)
        title.to_edge(UP)
        unit_square = Square(side_length=2, color=WHITE, fill_opacity=0.2)
        unit_square.move_to(ORIGIN)
        vector_i = Arrow(ORIGIN, RIGHT, color=RED, buff=0)
        vector_j = Arrow(ORIGIN, UP, color=BLUE, buff=0)
        label_i = Text("i", font_size=24, color=RED).next_to(vector_i.get_end(), RIGHT, buff=0.1)
        label_j = Text("j", font_size=24, color=BLUE).next_to(vector_j.get_end(), UP, buff=0.1)
        basis_text = Text("Basis Vectors", font_size=30).shift(DOWN * 2.5)

        self.play(FadeIn(title, scale=0.8), run_time=1)
        self.play(ShowCreation(unit_square), run_time=1)
        self.play(ShowCreation(vector_i), ShowCreation(vector_j), run_time=1)
        self.play(FadeIn(label_i), FadeIn(label_j), run_time=0.5)
        self.play(FadeIn(basis_text, shift=UP * 0.3), run_time=0.8)
        self.wait(1)

        # Act 2: Transforming the Unit Square
        scaling_text = Text("Scaling", font_size=40).to_edge(UP)
        rotation_text = Text("Rotation", font_size=40).to_edge(UP)
        shear_text = Text("Shear", font_size=40).to_edge(UP)
        reflection_text = Text("Reflection", font_size=40).to_edge(UP)

        self.play(FadeOut(title), FadeOut(basis_text), run_time=0.5)
        self.play(FadeIn(scaling_text, shift=UP * 0.3), run_time=0.5)
        self.play(
            ApplyMethod(unit_square.apply_matrix, [[2, 0], [0, 0.5]]),
            ApplyMethod(vector_i.apply_matrix, [[2, 0], [0, 0.5]]),
            ApplyMethod(vector_j.apply_matrix, [[2, 0], [0, 0.5]]),
            ApplyMethod(label_i.move_to, vector_i.get_end() + RIGHT * 0.1),
            ApplyMethod(label_j.move_to, vector_j.get_end() + UP * 0.1),
            run_time=2
        )
        self.wait(0.5)
        unit_square.apply_matrix([[0.5, 0], [0, 2]])  # Reset
        vector_i.apply_matrix([[0.5, 0], [0, 2]])
        vector_j.apply_matrix([[0.5, 0], [0, 2]])
        label_i.move_to(vector_i.get_end() + RIGHT * 0.1)
        label_j.move_to(vector_j.get_end() + UP * 0.1)

        self.play(FadeOut(scaling_text), FadeIn(rotation_text, shift=UP * 0.3), run_time=0.5)
        self.play(
            ApplyMethod(unit_square.apply_matrix, [[0.707, -0.707], [0.707, 0.707]]),
            ApplyMethod(vector_i.apply_matrix, [[0.707, -0.707], [0.707, 0.707]]),
            ApplyMethod(vector_j.apply_matrix, [[0.707, -0.707], [0.707, 0.707]]),
            ApplyMethod(label_i.move_to, vector_i.get_end() + RIGHT * 0.1),
            ApplyMethod(label_j.move_to, vector_j.get_end() + UP * 0.1),
            run_time=2
        )
        self.wait(0.5)
        unit_square.apply_matrix([[0.707, 0.707], [-0.707, 0.707]])  # Reset
        vector_i.apply_matrix([[0.707, 0.707], [-0.707, 0.707]])
        vector_j.apply_matrix([[0.707, 0.707], [-0.707, 0.707]])
        label_i.move_to(vector_i.get_end() + RIGHT * 0.1)
        label_j.move_to(vector_j.get_end() + UP * 0.1)

        self.play(FadeOut(rotation_text), FadeIn(shear_text, shift=UP * 0.3), run_time=0.5)
        self.play(
            ApplyMethod(unit_square.apply_matrix, [[1, 1], [0, 1]]),
            ApplyMethod(vector_i.apply_matrix, [[1, 1], [0, 1]]),
            ApplyMethod(vector_j.apply_matrix, [[1, 1], [0, 1]]),
            ApplyMethod(label_i.move_to, vector_i.get_end() + RIGHT * 0.1),
            ApplyMethod(label_j.move_to, vector_j.get_end() + UP * 0.1),
            run_time=2
        )
        self.wait(0.5)
        unit_square.apply_matrix([[1, -1], [0, 1]])  # Reset
        vector_i.apply_matrix([[1, -1], [0, 1]])
        vector_j.apply_matrix([[1, -1], [0, 1]])
        label_i.move_to(vector_i.get_end() + RIGHT * 0.1)
        label_j.move_to(vector_j.get_end() + UP * 0.1)

        self.play(FadeOut(shear_text), FadeIn(reflection_text, shift=UP * 0.3), run_time=0.5)
        self.play(
            ApplyMethod(unit_square.apply_matrix, [[-1, 0], [0, 1]]),
            ApplyMethod(vector_i.apply_matrix, [[-1, 0], [0, 1]]),
            ApplyMethod(vector_j.apply_matrix, [[-1, 0], [0, 1]]),
            ApplyMethod(label_i.move_to, vector_i.get_end() + LEFT * 0.1),
            ApplyMethod(label_j.move_to, vector_j.get_end() + UP * 0.1),
            run_time=2
        )
        self.wait(0.5)

        # Act 3: Grid Deformation
        grid_text = Text("Grid Deformation", font_size=40).to_edge(UP)
        grid = VGroup()
        for x in range(-2, 3):
            grid.add(Line(LEFT * 2 + UP * x, RIGHT * 2 + UP * x, color=GREY, stroke_width=1))
            grid.add(Line(UP * 2 + LEFT * x, DOWN * 2 + LEFT * x, color=GREY, stroke_width=1))
        grid.move_to(ORIGIN)

        self.play(FadeOut(unit_square), FadeOut(vector_i), FadeOut(vector_j), FadeOut(label_i), FadeOut(label_j), FadeOut(reflection_text), run_time=0.5)
        self.play(FadeIn(grid_text, shift=UP * 0.3), run_time=0.5)
        self.play(ShowCreation(grid), run_time=1.5)
        self.play(ApplyMethod(grid.apply_matrix, [[2, 0], [0, 0.5]]), run_time=2)
        grid.apply_matrix([[0.5, 0], [0, 2]])  # Reset
        self.play(ApplyMethod(grid.apply_matrix, [[0.707, -0.707], [0.707, 0.707]]), run_time=2)
        grid.apply_matrix([[0.707, 0.707], [-0.707, 0.707]])  # Reset
        self.play(ApplyMethod(grid.apply_matrix, [[1, 1], [0, 1]]), run_time=2)
        grid.apply_matrix([[1, -1], [0, 1]])  # Reset
        self.play(ApplyMethod(grid.apply_matrix, [[-1, 0], [0, 1]]), run_time=2)
        self.wait(0.5)

        # Act 4: Points Following Basis Vectors
        points_text = Text("Points Follow Basis", font_size=40).to_edge(UP)
        dot_p = Dot(point=RIGHT * 1.5 + UP * 0.5, color=YELLOW, radius=0.1)
        vector_i_new = Arrow(ORIGIN, RIGHT, color=RED, buff=0)
        vector_j_new = Arrow(ORIGIN, UP, color=BLUE, buff=0)
        label_i_new = Text("i", font_size=24, color=RED).next_to(vector_i_new.get_end(), RIGHT, buff=0.1)
        label_j_new = Text("j", font_size=24, color=BLUE).next_to(vector_j_new.get_end(), UP, buff=0.1)

        self.play(FadeOut(grid_text), run_time=0.5)
        self.play(FadeIn(points_text, shift=UP * 0.3), run_time=0.5)
        self.play(ShowCreation(dot_p), run_time=0.5)
        self.play(ShowCreation(vector_i_new), ShowCreation(vector_j_new), FadeIn(label_i_new), FadeIn(label_j_new), run_time=1)
        self.play(
            ApplyMethod(grid.apply_matrix, [[0.707, -0.707], [0.707, 0.707]]),
            ApplyMethod(vector_i_new.apply_matrix, [[0.707, -0.707], [0.707, 0.707]]),
            ApplyMethod(vector_j_new.apply_matrix, [[0.707, -0.707], [0.707, 0.707]]),
            ApplyMethod(dot_p.apply_matrix, [[0.707, -0.707], [0.707, 0.707]]),
            ApplyMethod(label_i_new.move_to, vector_i_new.get_end() + RIGHT * 0.1),
            ApplyMethod(label_j_new.move_to, vector_j_new.get_end() + UP * 0.1),
            run_time=2
        )
        self.play(Indicate(dot_p, color=YELLOW), run_time=1)
        self.wait(0.5)

        # Act 5: Matrix Multiplication as Composition
        comp_text = Text("Composition of Transformations", font_size=40).to_edge(UP)
        matrix_a_text = Text("Matrix A", font_size=30).shift(DOWN * 2.5)
        matrix_b_text = Text("Matrix B", font_size=30).shift(DOWN * 2.5)
        combined_text = Text("A then B", font_size=30).shift(DOWN * 2.5)

        self.play(FadeOut(points_text), FadeOut(dot_p), FadeOut(vector_i_new), FadeOut(vector_j_new), FadeOut(label_i_new), FadeOut(label_j_new), run_time=0.5)
        self.play(FadeIn(comp_text, shift=UP * 0.3), run_time=0.5)
        self.play(FadeIn(matrix_a_text, shift=UP * 0.3), run_time=0.5)
        self.play(ApplyMethod(grid.apply_matrix, [[2, 0], [0, 0.5]]), run_time=2)
        self.play(FadeOut(matrix_a_text), FadeIn(matrix_b_text, shift=UP * 0.3), run_time=0.5)
        self.play(ApplyMethod(grid.apply_matrix, [[0.707, -0.707], [0.707, 0.707]]), run_time=2)
        self.play(FadeOut(matrix_b_text), FadeIn(combined_text, shift=UP * 0.3), run_time=0.5)
        grid.apply_matrix([[0.354, 0.354], [-0.707, 0.707]])  # Reset
        self.play(ApplyMethod(grid.apply_matrix, [[1.414, -1.414], [0.707, 0.354]]), run_time=2)
        self.wait(0.5)

        # Act 6: Determinants and Area Scaling
        det_text = Text("Determinant = Area Scaling", font_size=40).to_edge(UP)
        unit_square_new = Square(side_length=2, color=WHITE, fill_opacity=0.2)
        unit_square_new.move_to(ORIGIN)
        area_before = Text("Area: 1 unit²", font_size=30).shift(DOWN * 2.5)
        area_after = Text("Area: 2 units²", font_size=30).shift(DOWN * 2.5)

        self.play(FadeOut(grid), FadeOut(comp_text), FadeOut(combined_text), run_time=0.5)
        self.play(FadeIn(det_text, shift=UP * 0.3), run_time=0.5)
        self.play(ShowCreation(unit_square_new), run_time=1)
        self.play(FadeIn(area_before, shift=UP * 0.3), run_time=0.5)
        self.play(ApplyMethod(unit_square_new.apply_matrix, [[2, 0], [0, 1]]), run_time=2)
        self.play(FadeOut(area_before), FadeIn(area_after, shift=UP * 0.3), run_time=0.5)
        self.wait(0.5)

        # Closing: Eigenvectors
        eig_text = Text("Eigenvectors: Invariant Directions", font_size=40).to_edge(UP)
        vector_eig = Arrow(ORIGIN, RIGHT * 2, color=GREEN, buff=0)

        self.play(FadeOut(det_text), FadeOut(area_after), run_time=0.5)
        self.play(FadeIn(eig_text, shift=UP * 0.3), run_time=0.5)
        self.play(ShowCreation(vector_eig), run_time=1)
        self.play(
            ApplyMethod(unit_square_new.apply_matrix, [[2, 0], [0, 1]]),
            ApplyMethod(vector_eig.apply_matrix, [[2, 0], [0, 1]]),
            run_time=2
        )
        self.wait(0.5)
        self.play(FadeOut(unit_square_new), FadeOut(vector_eig), FadeOut(eig_text), run_time=1.5)