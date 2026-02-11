from manimlib import *

class GeneratedScene(Scene):
    def construct(self):
        # ── Act 1: Introduction & Triangle Setup (~10s) ─────────────────────────
        title = Text("Pythagorean Theorem", font_size=60)
        self.play(FadeIn(title, scale=0.8), run_time=1)
        self.wait(1.5)
        self.play(title.animate.scale(0.5).to_edge(UP), run_time=0.8)

        # Define triangle vertices (small to fit squares on screen)
        A = np.array([-1.5, -1, 0])  # Right angle
        B = np.array([1.5, -1, 0])   # Bottom right
        C = np.array([-1.5, 1, 0])   # Top left

        # Triangle sides with consistent colors
        side_a = Line(B, C, color=BLUE)    # Hypotenuse
        side_b = Line(A, B, color=GREEN)   # Base
        side_c = Line(A, C, color=RED)     # Vertical

        # Right angle marker, precisely aligned
        right_angle_marker = Square(side_length=0.3, color=WHITE)
        right_angle_marker.move_to(A)
        right_angle_marker.align_to(A, DL)

        # Side labels
        label_a = Text("a", font_size=30, color=BLUE)
        label_a.move_to(side_a.get_center() + normalize(np.array([-side_a.get_end()[1] + side_a.get_start()[1], side_a.get_end()[0] - side_a.get_start()[0], 0])) * 0.3)
        label_b = Text("b", font_size=30, color=GREEN)
        label_b.next_to(side_b.get_center(), DOWN, buff=0.2)
        label_c = Text("c", font_size=30, color=RED)
        label_c.next_to(side_c.get_center(), LEFT, buff=0.2)

        self.play(ShowCreation(side_b), ShowCreation(side_c), ShowCreation(side_a), run_time=1.5)
        self.play(FadeIn(label_a), FadeIn(label_b), FadeIn(label_c), run_time=0.8)
        self.play(ShowCreation(right_angle_marker), run_time=0.8)
        self.wait(2.5)  # Let narrator explain

        # ── Act 2: Squares on Sides (~15s) ─────────────────────────
        # Square on side b (base AB)
        side_b_vec = B - A
        side_b_length = np.linalg.norm(side_b_vec)
        perp_b_unit = normalize(np.array([-side_b_vec[1], side_b_vec[0], 0]))
        perp_b = perp_b_unit * side_b_length
        P_b1 = A + perp_b
        P_b2 = B + perp_b
        square_b = Polygon(A, B, P_b2, P_b1, color=GREEN, fill_opacity=0.3, stroke_width=2)
        label_b_sq = Text("b²", font_size=30, color=GREEN)
        label_b_sq.move_to(square_b.get_center())

        self.play(ShowCreation(square_b), run_time=1.2)
        self.play(FadeIn(label_b_sq, shift=UP * 0.3), run_time=0.6)
        self.wait(1.5)

        # Square on side c (vertical AC)
        side_c_vec = C - A
        side_c_length = np.linalg.norm(side_c_vec)
        perp_c_unit = normalize(np.array([-side_c_vec[1], side_c_vec[0], 0]))
        perp_c = perp_c_unit * side_c_length
        P_c1 = A + perp_c
        P_c2 = C + perp_c
        square_c = Polygon(A, C, P_c2, P_c1, color=RED, fill_opacity=0.3, stroke_width=2)
        label_c_sq = Text("c²", font_size=30, color=RED)
        label_c_sq.move_to(square_c.get_center())

        self.play(ShowCreation(square_c), run_time=1.2)
        self.play(FadeIn(label_c_sq, shift=UP * 0.3), run_time=0.6)
        self.wait(1.5)

        # Square on side a (hypotenuse BC), outward
        side_a_vec = C - B
        side_a_length = np.linalg.norm(side_a_vec)
        perp_a_unit = normalize(np.array([-side_a_vec[1], side_a_vec[0], 0]))
        centroid = (A + B + C) / 3
        if np.dot(perp_a_unit, centroid - side_a.get_center()) > 0:
            perp_a_unit = -perp_a_unit
        perp_a = perp_a_unit * side_a_length
        P_a1 = B + perp_a
        P_a2 = C + perp_a
        square_a = Polygon(B, C, P_a2, P_a1, color=BLUE, fill_opacity=0.3, stroke_width=2)
        label_a_sq = Text("a²", font_size=30, color=BLUE)
        label_a_sq.move_to(square_a.get_center())

        self.play(ShowCreation(square_a), run_time=1.2)
        self.play(FadeIn(label_a_sq, shift=UP * 0.3), run_time=0.6)
        self.wait(1.5)

        # ── Act 3: Visual Proof & Equation (~15s) ─────────────────────────
        self.play(
            Indicate(square_b, scale_factor=1.1, color=YELLOW),
            Indicate(square_c, scale_factor=1.1, color=YELLOW),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(Indicate(square_a, scale_factor=1.1, color=YELLOW), run_time=1.5)
        self.wait(1.5)

        equation = Text("a² + b² = c²", font_size=40, color=WHITE)
        equation.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(equation, shift=UP * 0.3), run_time=1)
        self.wait(2.5)

        # ── Closing (~5s) ────────────────────────────────────────
        all_objs = VGroup(side_a, side_b, side_c, label_a, label_b, label_c, right_angle_marker,
                          square_a, square_b, square_c, label_a_sq, label_b_sq, label_c_sq, title)
        self.play(FadeOut(all_objs), run_time=1)
        self.wait(2)
        self.play(FadeOut(equation), run_time=1)