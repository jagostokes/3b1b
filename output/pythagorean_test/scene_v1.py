from manimlib import *

class GeneratedScene(Scene):
    def construct(self):
        # Color palette
        COLOR_A = BLUE
        COLOR_B = GREEN
        COLOR_C = RED
        TEXT_COLOR = WHITE

        # ── Act 1: Introduction & Triangle Setup (~10s) ─────────────────────────
        title = Text("The Pythagorean Theorem", font_size=60, color=TEXT_COLOR)
        self.play(FadeIn(title, scale=0.8), run_time=1)
        self.wait(1.5)
        self.play(title.animate.scale(0.5).to_edge(UP), run_time=0.8)

        # Define triangle vertices
        A = DOWN * 2 + LEFT * 3
        B = DOWN * 2 + RIGHT * 2
        C = UP * 2 + LEFT * 3

        # Create right triangle
        triangle = Polygon(A, B, C, color=WHITE)
        triangle.set_stroke(width=3)

        # Label sides
        label_a = Text("a", font_size=30, color=COLOR_A)
        label_a.next_to(Line(B, C).get_center(), RIGHT, buff=0.2)
        label_b = Text("b", font_size=30, color=COLOR_B)
        label_b.next_to(Line(A, B).get_center(), DOWN, buff=0.2)
        label_c = Text("c", font_size=30, color=COLOR_C)
        label_c.next_to(Line(A, C).get_center(), LEFT, buff=0.2)

        self.play(ShowCreation(triangle), run_time=1.5)
        self.play(FadeIn(label_a), FadeIn(label_b), FadeIn(label_c), run_time=0.8)
        self.wait(1.5)

        # ── Act 2: Squares on Sides (~15s) ───────────────────────────────
        # Square on side a (between B and C)
        side_a = Line(B, C)
        square_a = Square(side_length=side_a.get_length())
        square_a.set_stroke(color=COLOR_A, width=2)
        square_a.set_fill(COLOR_A, opacity=0.2)
        square_a.move_to(side_a.get_center())
        square_a.rotate(side_a.get_angle() + PI/2, about_point=side_a.get_center())
        square_a.shift(RIGHT * 0.5 * side_a.get_length())

        # Square on side b (between A and B)
        side_b = Line(A, B)
        square_b = Square(side_length=side_b.get_length())
        square_b.set_stroke(color=COLOR_B, width=2)
        square_b.set_fill(COLOR_B, opacity=0.2)
        square_b.move_to(side_b.get_center())
        square_b.rotate(side_b.get_angle() + PI/2, about_point=side_b.get_center())
        square_b.shift(DOWN * 0.5 * side_b.get_length())

        # Square on side c (between A and C)
        side_c = Line(A, C)
        square_c = Square(side_length=side_c.get_length())
        square_c.set_stroke(color=COLOR_C, width=2)
        square_c.set_fill(COLOR_C, opacity=0.2)
        square_c.move_to(side_c.get_center())
        square_c.rotate(side_c.get_angle() + PI/2, about_point=side_c.get_center())
        square_c.shift(LEFT * 0.5 * side_c.get_length())

        # Area labels for squares
        area_a = Text("a\u00b2", font_size=30, color=COLOR_A)
        area_a.next_to(square_a.get_center(), RIGHT, buff=0.2)
        area_b = Text("b\u00b2", font_size=30, color=COLOR_B)
        area_b.next_to(square_b.get_center(), DOWN, buff=0.2)
        area_c = Text("c\u00b2", font_size=30, color=COLOR_C)
        area_c.next_to(square_c.get_center(), LEFT, buff=0.2)

        self.play(LaggedStart(
            ShowCreation(square_a),
            ShowCreation(square_b),
            ShowCreation(square_c),
            lag_ratio=0.3
        ), run_time=3)
        self.play(FadeIn(area_a, shift=RIGHT*0.3), FadeIn(area_b, shift=DOWN*0.3), FadeIn(area_c, shift=LEFT*0.3), run_time=1)
        self.wait(2)

        # ── Act 3: Visual Proof (~15s) ───────────────────────────────
        # Create equation components
        equation_a = Text("a\u00b2", font_size=40, color=COLOR_A)
        equation_plus = Text("+", font_size=40, color=TEXT_COLOR)
        equation_b = Text("b\u00b2", font_size=40, color=COLOR_B)
        equation_equals = Text("=", font_size=40, color=TEXT_COLOR)
        equation_c = Text("c\u00b2", font_size=40, color=COLOR_C)
        equation = VGroup(equation_a, equation_plus, equation_b, equation_equals, equation_c)
        equation.arrange(RIGHT, buff=0.3)
        equation.to_edge(DOWN, buff=1)

        self.play(
            FadeTransform(area_a.copy(), equation_a),
            FadeTransform(area_b.copy(), equation_b),
            FadeTransform(area_c.copy(), equation_c),
            FadeIn(equation_plus, scale=0.8),
            FadeIn(equation_equals, scale=0.8),
            run_time=2
        )
        self.wait(1.5)
        self.play(Indicate(equation, color=YELLOW), run_time=1.5)
        self.wait(1.5)

        # ── Closing (~5s) ────────────────────────────────────────
        all_objs = VGroup(triangle, label_a, label_b, label_c, square_a, square_b, square_c, area_a, area_b, area_c, equation, title)
        closing = Text("The Pythagorean Theorem:\na\u00b2 + b\u00b2 = c\u00b2", font_size=44, color=TEXT_COLOR)

        self.play(FadeOut(all_objs), run_time=1)
        self.play(FadeIn(closing, scale=0.9), run_time=1)
        self.wait(2)
        self.play(FadeOut(closing), run_time=1)