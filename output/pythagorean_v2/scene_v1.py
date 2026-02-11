from manimlib import *

class GeneratedScene(Scene):
    def construct(self):
        # ── Act 1: Introduction & Triangle Setup (~10s) ─────────────────────────
        title = Text("Pythagorean Theorem", font_size=60)
        self.play(FadeIn(title, scale=0.8), run_time=1)
        self.wait(1.5)
        self.play(title.animate.scale(0.5).to_edge(UP), run_time=0.8)

        # Define triangle vertices (small scale to fit squares on screen)
        A = np.array([-1.5, -1, 0])  # Bottom-left (right angle)
        B = np.array([1.5, -1, 0])   # Bottom-right
        C = np.array([-1.5, 1, 0])   # Top-left

        # Triangle sides with consistent colors
        side_a = Line(B, C, color=BLUE)   # Leg a (vertical)
        side_b = Line(A, B, color=GREEN)  # Leg b (horizontal)
        side_c = Line(A, C, color=RED)    # Hypotenuse c

        # Right angle marker at A
        right_angle_marker = Square(side_length=0.3)
        right_angle_marker.move_to(A)
        right_angle_marker.align_to(A, DL)

        # Labels for sides
        label_a = Text("a", font_size=30, color=BLUE)
        label_a.next_to(side_a.get_center(), RIGHT, buff=0.2)
        label_b = Text("b", font_size=30, color=GREEN)
        label_b.next_to(side_b.get_center(), DOWN, buff=0.2)
        label_c = Text("c", font_size=30, color=RED)
        label_c.next_to(side_c.get_center(), UL, buff=0.2)

        # Animate triangle creation
        self.play(ShowCreation(side_a), run_time=1)
        self.play(ShowCreation(side_b), run_time=1)
        self.play(ShowCreation(side_c), run_time=1)
        self.play(ShowCreation(right_angle_marker), run_time=0.5)
        self.play(FadeIn(label_a), FadeIn(label_b), FadeIn(label_c), run_time=0.8)
        self.wait(2)

        # ── Act 2: Building Squares on Sides (~12s) ─────────────────────────
        # Square on side a (BLUE) - inward toward triangle center
        side_a_vec = C - B
        perp_a = normalize(np.array([-side_a_vec[1], side_a_vec[0], 0]))
        centroid = (A + B + C) / 3
        if np.dot(perp_a, centroid - side_a.get_center()) < 0:
            perp_a = -perp_a
        square_a = Square(side_length=np.linalg.norm(side_a_vec), color=BLUE)
        square_a.set_fill(BLUE, opacity=0.3)
        square_a.move_to(side_a.get_center() + perp_a * np.linalg.norm(side_a_vec) / 2)
        label_a_sq = Text("a²", font_size=30, color=BLUE)
        label_a_sq.move_to(square_a.get_center())

        # Square on side b (GREEN) - inward
        side_b_vec = B - A
        perp_b = normalize(np.array([-side_b_vec[1], side_b_vec[0], 0]))
        if np.dot(perp_b, centroid - side_b.get_center()) < 0:
            perp_b = -perp_b
        square_b = Square(side_length=np.linalg.norm(side_b_vec), color=GREEN)
        square_b.set_fill(GREEN, opacity=0.3)
        square_b.move_to(side_b.get_center() + perp_b * np.linalg.norm(side_b_vec) / 2)
        label_b_sq = Text("b²", font_size=30, color=GREEN)
        label_b_sq.move_to(square_b.get_center())

        # Square on side c (RED) - inward
        side_c_vec = C - A
        perp_c = normalize(np.array([-side_c_vec[1], side_c_vec[0], 0]))
        if np.dot(perp_c, centroid - side_c.get_center()) < 0:
            perp_c = -perp_c
        square_c = Square(side_length=np.linalg.norm(side_c_vec), color=RED)
        square_c.set_fill(RED, opacity=0.3)
        square_c.move_to(side_c.get_center() + perp_c * np.linalg.norm(side_c_vec) / 2)
        label_c_sq = Text("c²", font_size=30, color=RED)
        label_c_sq.move_to(square_c.get_center())

        # Animate squares and labels
        self.play(ShowCreation(square_a), run_time=1.2)
        self.play(FadeIn(label_a_sq), run_time=0.6)
        self.wait(1)
        self.play(ShowCreation(square_b), run_time=1.2)
        self.play(FadeIn(label_b_sq), run_time=0.6)
        self.wait(1)
        self.play(ShowCreation(square_c), run_time=1.2)
        self.play(FadeIn(label_c_sq), run_time=0.6)
        self.wait(1.5)

        # ── Act 3: Visual Proof of a² + b² = c² (~15s) ─────────────────────────
        self.play(
            Indicate(square_a, scale_factor=1.1, color=YELLOW),
            Indicate(square_b, scale_factor=1.1, color=YELLOW),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(Indicate(square_c, scale_factor=1.1, color=YELLOW), run_time=1.5)
        self.wait(1)

        equation = Text("a² + b² = c²", font_size=40)
        equation.to_edge(DOWN)
        self.play(FadeIn(equation), run_time=1)
        self.wait(2)

        # ── Closing (~8s) ───────────────────────────────────────────────
        all_objs = VGroup(
            side_a, side_b, side_c, right_angle_marker,
            label_a, label_b, label_c,
            square_a, square_b, square_c,
            label_a_sq, label_b_sq, label_c_sq,
            equation, title
        )
        closing = Text("a² + b² = c²", font_size=50)

        self.play(FadeOut(all_objs), run_time=1)
        self.play(FadeIn(closing, scale=0.9), run_time=1)
        self.wait(2)
        self.play(FadeOut(closing), run_time=1)