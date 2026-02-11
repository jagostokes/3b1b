from manimlib import *

class GeneratedScene(Scene):
    def construct(self):
        # ACT 1: Introduction to Linear Transformations
        title = Text("Linear Transformations as Space Movers", font_size=50)
        title.to_edge(UP)
        unit_square = Square(side_length=2, color=WHITE, fill_opacity=0.2)
        unit_square.move_to(ORIGIN)
        vector_i = Arrow(ORIGIN, RIGHT, color=RED, buff=0)
        vector_j = Arrow(ORIGIN, UP, color=BLUE, buff=0)
        label_i = Text("i", font_size=24, color=RED).next_to(vector_i.get_end(), RIGHT, buff=0.1)
        label_j = Text("j", font_size=24, color=BLUE).next_to(vector_j.get_end(), UP, buff=0.1)
        basis_text = Text("Basis Vectors", font_size=30).next_to(unit_square, DOWN, buff=0.5)

        self.play(FadeIn(title, scale=0.8), run_time=1)
        self.play(ShowCreation(unit_square), run_time=1)
        self.play(ShowCreation(vector_i), ShowCreation(vector_j), run_time=1)
        self.play(FadeIn(label_i), FadeIn(label_j), run_time=0.5)
        self.play(FadeIn(basis_text, shift=UP*0.3), run_time=0.8)
        self.wait(1)

        # ACT 2: Transforming the Unit Square
        scaling_text = Text("Scaling", font_size=40).to_edge(UP)
        rotation_text = Text("Rotation", font_size=40).to_edge(UP)
        shear_text = Text("Shear", font_size=40).to_edge(UP)
        reflection_text = Text("Reflection", font_size=40).to_edge(UP)

        self.play(FadeOut(title), FadeOut(basis_text), FadeIn(scaling_text), run_time=1)
        self.play(
            ApplyMethod(unit_square.apply_matrix, [[2, 0], [0, 1]]),
            ApplyMethod(vector_i.apply_matrix, [[2, 0], [0, 1]]),
            ApplyMethod(vector_j.apply_matrix, [[2, 0], [0, 1]]),
            label_i.animate.move_to(vector_i.get_end() + RIGHT*0.1),
            label_j.animate.move_to(vector_j.get_end() + UP*0.1),
            run_time=2
        )
        self.wait(0.5)
        self.play(
            ApplyMethod(unit_square.apply_matrix, [[0.5, 0], [0, 1]]),
            ApplyMethod(vector_i.apply_matrix, [[0.5, 0], [0, 1]]),
            ApplyMethod(vector_j.apply_matrix, [[0.5, 0], [0, 1]]),
            label_i.animate.move_to(vector_i.get_end() + RIGHT*0.1),
            label_j.animate.move_to(vector_j.get_end() + UP*0.1),
            FadeOut(scaling_text), FadeIn(rotation_text),
            run_time=1
        )
        self.play(
            Rotate(unit_square, PI/4),
            Rotate(vector_i, PI/4),
            Rotate(vector_j, PI/4),
            label_i.animate.move_to(vector_i.get_end() + RIGHT*0.1),
            label_j.animate.move_to(vector_j.get_end() + UP*0.1),
            run_time=2
        )
        self.wait(0.5)
        self.play(
            Rotate(unit_square, -PI/4),
            Rotate(vector_i, -PI/4),
            Rotate(vector_j, -PI/4),
            label_i.animate.move_to(vector_i.get_end() + RIGHT*0.1),
            label_j.animate.move_to(vector_j.get_end() + UP*0.1),
            FadeOut(rotation_text), FadeIn(shear_text),
            run_time=1
        )
        self.play(
            ApplyMethod(unit_square.apply_matrix, [[1, 1], [0, 1]]),
            ApplyMethod(vector_i.apply_matrix, [[1, 1], [0, 1]]),
            ApplyMethod(vector_j.apply_matrix, [[1, 1], [0, 1]]),
            label_i.animate.move_to(vector_i.get_end() + RIGHT*0.1),
            label_j.animate.move_to(vector_j.get_end() + UP*0.1),
            run_time=2
        )
        self.wait(0.5)
        self.play(
            ApplyMethod(unit_square.apply_matrix, [[1, -1], [0, 1]]),
            ApplyMethod(vector_i.apply_matrix, [[1, -1], [0, 1]]),
            ApplyMethod(vector_j.apply_matrix, [[1, -1], [0, 1]]),
            label_i.animate.move_to(vector_i.get_end() + RIGHT*0.1),
            label_j.animate.move_to(vector_j.get_end() + UP*0.1),
            FadeOut(shear_text), FadeIn(reflection_text),
            run_time=1
        )
        self.play(
            ApplyMethod(unit_square.apply_matrix, [[-1, 0], [0, 1]]),
            ApplyMethod(vector_i.apply_matrix, [[-1, 0], [0, 1]]),
            ApplyMethod(vector_j.apply_matrix, [[-1, 0], [0, 1]]),
            label_i.animate.move_to(vector_i.get_end() + RIGHT*0.1),
            label_j.animate.move_to(vector_j.get_end() + UP*0.1),
            run_time=2
        )
        self.wait(0.5)
        self.play(
            ApplyMethod(unit_square.apply_matrix, [[-1, 0], [0, 1]]),
            ApplyMethod(vector_i.apply_matrix, [[-1, 0], [0, 1]]),
            ApplyMethod(vector_j.apply_matrix, [[-1, 0], [0, 1]]),
            label_i.animate.move_to(vector_i.get_end() + RIGHT*0.1),
            label_j.animate.move_to(vector_j.get_end() + UP*0.1),
            FadeOut(reflection_text),
            run_time=1
        )

        # ACT 3: Grid Deformation and Point Movement
        grid = NumberPlane(x_range=(-3, 3, 1), y_range=(-3, 3, 1), width=6, height=6)
        grid.set_stroke(color=GREY, opacity=0.3)
        dots = VGroup(*[Dot(np.array([x, y, 0]), radius=0.05) for x in range(-2, 3) for y in range(-2, 3)])
        points_text = Text("Points Follow Basis", font_size=40).to_edge(UP)

        self.play(ShowCreation(grid), run_time=1.5)
        self.play(ShowCreation(dots), run_time=1)
        self.play(FadeIn(points_text, shift=UP*0.3), run_time=0.8)
        self.play(
            ApplyMethod(unit_square.apply_matrix, [[1.5, 0], [0, 1.5]]),
            ApplyMethod(vector_i.apply_matrix, [[1.5, 0], [0, 1.5]]),
            ApplyMethod(vector_j.apply_matrix, [[1.5, 0], [0, 1.5]]),
            ApplyMethod(grid.apply_matrix, [[1.5, 0], [0, 1.5]]),
            ApplyMethod(dots.apply_matrix, [[1.5, 0], [0, 1.5]]),
            Rotate(unit_square, PI/6),
            Rotate(vector_i, PI/6),
            Rotate(vector_j, PI/6),
            Rotate(grid, PI/6),
            Rotate(dots, PI/6),
            label_i.animate.move_to(vector_i.get_end() + RIGHT*0.1),
            label_j.animate.move_to(vector_j.get_end() + UP*0.1),
            run_time=3
        )
        self.wait(1)

        # ACT 4: Matrix Multiplication as Composition
        comp_text = Text("Composition of Transformations", font_size=40).to_edge(UP)
        first_text = Text("First Transform", font_size=30).next_to(unit_square, DOWN, buff=0.5)
        then_text = Text("Then Transform", font_size=30).next_to(unit_square, DOWN, buff=0.5)

        self.play(FadeOut(points_text), FadeIn(comp_text), run_time=1)
        self.play(FadeIn(first_text, shift=UP*0.3), run_time=0.8)
        self.play(
            Rotate(unit_square, PI/6),
            Rotate(vector_i, PI/6),
            Rotate(vector_j, PI/6),
            Rotate(grid, PI/6),
            label_i.animate.move_to(vector_i.get_end() + RIGHT*0.1),
            label_j.animate.move_to(vector_j.get_end() + UP*0.1),
            run_time=2
        )
        self.play(FadeOut(first_text), FadeIn(then_text), run_time=0.8)
        self.play(
            ApplyMethod(unit_square.apply_matrix, [[1.5, 0], [0, 1.5]]),
            ApplyMethod(vector_i.apply_matrix, [[1.5, 0], [0, 1.5]]),
            ApplyMethod(vector_j.apply_matrix, [[1.5, 0], [0, 1.5]]),
            ApplyMethod(grid.apply_matrix, [[1.5, 0], [0, 1.5]]),
            label_i.animate.move_to(vector_i.get_end() + RIGHT*0.1),
            label_j.animate.move_to(vector_j.get_end() + UP*0.1),
            run_time=2
        )
        self.wait(1)

        # ACT 5: Determinants and Area Scaling
        det_text = Text("Determinant = Area Scaling", font_size=40).to_edge(UP)
        area_before_text = Text("Area Before", font_size=30).next_to(unit_square, LEFT, buff=0.5)
        area_after_text = Text("Area After", font_size=30).next_to(unit_square, LEFT, buff=0.5)
        area_label_before = Text("1.0", font_size=24).next_to(area_before_text, DOWN, buff=0.2)
        area_label_after = Text("1.0", font_size=24).next_to(area_after_text, DOWN, buff=0.2)

        self.play(FadeOut(comp_text), FadeOut(then_text), FadeIn(det_text), run_time=1)
        self.play(FadeIn(area_before_text), FadeIn(area_label_before), run_time=0.8)
        self.play(
            ApplyMethod(unit_square.apply_matrix, [[2, 0], [0, 0.5]]),
            ApplyMethod(vector_i.apply_matrix, [[2, 0], [0, 0.5]]),
            ApplyMethod(vector_j.apply_matrix, [[2, 0], [0, 0.5]]),
            ApplyMethod(grid.apply_matrix, [[2, 0], [0, 0.5]]),
            label_i.animate.move_to(vector_i.get_end() + RIGHT*0.1),
            label_j.animate.move_to(vector_j.get_end() + UP*0.1),
            run_time=2
        )
        self.play(FadeIn(area_after_text), FadeOut(area_label_before), FadeIn(area_label_after), run_time=0.8)
        self.wait(1)

        # ACT 6: Eigenvectors and Invariant Directions
        eigen_text = Text("Eigenvectors: Invariant Directions", font_size=40).to_edge(UP)
        eigen_vector = Arrow(ORIGIN, UP + RIGHT, color=GREEN, buff=0)
        eigen_label = Text("Eigenvector", font_size=24, color=GREEN).next_to(eigen_vector.get_end(), UR, buff=0.1)

        self.play(
            FadeOut(det_text), FadeOut(area_before_text), FadeOut(area_after_text), FadeOut(area_label_after),
            FadeIn(eigen_text), run_time=1
        )
        self.play(ShowCreation(eigen_vector), FadeIn(eigen_label), run_time=1)
        self.play(
            ApplyMethod(unit_square.apply_matrix, [[2, 0], [0, 1]]),
            ApplyMethod(vector_i.apply_matrix, [[2, 0], [0, 1]]),
            ApplyMethod(vector_j.apply_matrix, [[2, 0], [0, 1]]),
            ApplyMethod(grid.apply_matrix, [[2, 0], [0, 1]]),
            ApplyMethod(eigen_vector.apply_matrix, [[2, 0], [0, 1]]),
            label_i.animate.move_to(vector_i.get_end() + RIGHT*0.1),
            label_j.animate.move_to(vector_j.get_end() + UP*0.1),
            eigen_label.animate.move_to(eigen_vector.get_end() + UR*0.1),
            run_time=2
        )
        self.play(Indicate(eigen_vector, color=GREEN), run_time=1)
        self.wait(1)

        # CLOSING
        final_text = Text("Linear Transformations Shape Space", font_size=50).move_to(ORIGIN)
        self.play(
            FadeOut(unit_square), FadeOut(vector_i), FadeOut(vector_j), FadeOut(grid),
            FadeOut(dots), FadeOut(label_i), FadeOut(label_j), FadeOut(eigen_vector),
            FadeOut(eigen_label), FadeOut(eigen_text), run_time=1
        )
        self.play(FadeIn(final_text, scale=0.8), run_time=1)
        self.wait(2)
        self.play(FadeOut(final_text), run_time=1)