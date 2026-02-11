from manimlib import *

class GeneratedScene(Scene):
    def construct(self):

        # ── Act 1: Introduction to Graphs ───────────────
        axes = Axes(
            x_range=(-2, 2, 1), 
            y_range=(0, 4, 1),
            width=8, 
            height=4.5,
            axis_config=dict(stroke_color=GREY_A)
        )
        axes.shift(0.5 * DOWN)

        graph = axes.get_graph(lambda x: x**2, x_range=(-2, 2), color=BLUE)
        graph.set_stroke(width=3)

        label = Text("y=x²", font_size=30, color=BLUE)
        label.set_backstroke(color=BLACK, width=5)
        label.next_to(axes.i2gp(0, graph), UP, buff=0.3)

        self.play(ShowCreation(axes), run_time=1.5)
        self.play(ShowCreation(graph), run_time=1.5)
        self.play(Write(label), run_time=1.5)
        self.wait(2.5)
        self.play(Indicate(graph, color=YELLOW), run_time=1.0)
        self.wait(1.0)

        # ── Act 2: What is "Area Under the Curve"? ───────────────
        shaded_region = axes.get_area_under_graph(graph, x_range=(0, 1), fill_color=GREEN, fill_opacity=0.3)
        area_label = Text("Area", font_size=30, color=GREEN)
        area_label.set_backstroke(color=BLACK, width=5)
        pos = axes.c2p(0.5, 0)
        assert -4 < pos[1] < 4 and -7 < pos[0] < 7, "Label position out of bounds"
        area_label.next_to(pos, DOWN, buff=0.4)

        self.play(DrawBorderThenFill(shaded_region), run_time=2.0)
        self.play(Write(area_label), run_time=1.5)
        self.wait(2.0)  # Total act duration: ~6.5s
        self.play(Indicate(shaded_region, color=YELLOW), run_time=1.0)

        # ── Act 3: Intuition with Rectangles ───────────────
        rects_coarse = axes.get_riemann_rectangles(graph, x_range=(0, 1), dx=0.2, input_sample_type="left", colors=(YELLOW,), fill_opacity=0.5)
        approx_label = Text("Approximation", font_size=30, color=YELLOW)
        approx_label.set_backstroke(color=BLACK, width=5)
        approx_label.next_to(axes.c2p(0.3, 1), UP, buff=0.3)

        self.play(LaggedStartMap(ShowCreation, rects_coarse), run_time=2.5)
        self.play(Write(approx_label), run_time=1.5)
        self.play(Indicate(rects_coarse, color=WHITE), run_time=1.0)
        self.wait(3.0)  # Adjusted for pacing, total act duration: ~8s

        # Cleanup for next act
        self.play(FadeOut(rects_coarse), FadeOut(approx_label), run_time=1.0)

        # ── Act 4: Refining the Approximation ───────────────
        rects_fine = axes.get_riemann_rectangles(graph, x_range=(0, 1), dx=0.1, input_sample_type="left", colors=(YELLOW,), fill_opacity=0.5)
        better_approx_label = Text("Better Approximation", font_size=30, color=YELLOW)
        better_approx_label.set_backstroke(color=BLACK, width=5)
        # Confirmed: axes.c2p(0.3, 1) + UP*0.3 is within frame bounds [-7, 7] x [-4, 4]
        better_approx_label.next_to(axes.c2p(0.3, 1), UP, buff=0.3)

        rects_fine_group1 = rects_fine[:5]
        rects_fine_group2 = rects_fine[5:]
        self.play(LaggedStartMap(ShowCreation, rects_fine_group1), run_time=1.0)
        self.play(LaggedStartMap(ShowCreation, rects_fine_group2), run_time=1.0)
        self.play(Write(better_approx_label), run_time=1.5)
        self.wait(3.5)
        self.play(Indicate(better_approx_label, color=WHITE), run_time=1.0)
        self.play(FadeOut(rects_fine), FadeOut(better_approx_label), run_time=1.0)

        # ── Act 5: The Concept of Integration ───────────────
        integration_text = Text("Integration = Exact Area", font_size=40, color=RED)
        integration_text.to_edge(UP, buff=0.5)
        # Position within safe frame bounds [-7, 7] x [-4, 4]

        limit_text = Text("Limit as width → 0", font_size=30, color=YELLOW)
        limit_text.next_to(integration_text, DOWN, buff=0.5)

        thin_rects = axes.get_riemann_rectangles(graph, x_range=(0, 1), dx=0.05, input_sample_type="left", colors=(YELLOW,), fill_opacity=0.3)

        self.play(Write(integration_text), run_time=2.0)
        self.play(LaggedStartMap(ShowCreation, thin_rects), lag_ratio=0.2, run_time=2.0)
        self.play(Indicate(thin_rects, color=YELLOW), run_time=1.0)
        self.play(Write(limit_text), run_time=1.0)
        self.wait(2.5)
        self.play(FadeOut(thin_rects), FadeOut(integration_text), FadeOut(limit_text), run_time=1.0)

        # ── Act 6: Real-World Meaning ───────────────
        # Act 6: Real-World Meaning (~7s)
        meaning_text = Text("Area = Total Quantity", font_size=40, color=GREEN)
        meaning_text.to_edge(UP, buff=0.5)

        subtext = Text("e.g., Distance if y=Speed", font_size=30, color=GREEN)
        subtext.next_to(meaning_text, DOWN, buff=0.5)

        self.play(Write(meaning_text), run_time=1.5)
        self.play(Write(subtext), run_time=1.5)
        self.wait(4.0)

        self.play(FadeOut(meaning_text), FadeOut(subtext), run_time=1.0)

        # ── Act 7: Closing ───────────────
        closing_msg = Text("Area Under the Curve: From Approximation to Integration", font_size=44)
        closing_msg.move_to(ORIGIN)
        self.play(FadeIn(closing_msg, scale=0.9), run_time=1.0)
        self.play(Indicate(closing_msg, scale_factor=1.1), run_time=1.0)
        self.wait(3.0)
        self.play(FadeOut(axes), FadeOut(graph), FadeOut(label), FadeOut(shaded_region), FadeOut(area_label), FadeOut(closing_msg), run_time=1.0)
        self.wait(1.0)