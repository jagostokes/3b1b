from manimlib import *

class GeneratedScene(Scene):
    def construct(self):

        # ── Act 1: Introduction to Graphs ───────────────
        title = Text("Coordinate System", font_size=40, color=WHITE).to_edge(UP)
        axes = Axes(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            width=8,
            height=5,
            axis_config={"stroke_color": GREY_A}
        )
        axes.shift(0.5 * DOWN)
        label_x = Text("x", font_size=24, color=WHITE)
        label_x.next_to(axes.get_x_axis().get_end(), DOWN, buff=0.3)
        label_y = Text("y", font_size=24, color=WHITE)
        label_y.next_to(axes.get_y_axis().get_end(), LEFT, buff=0.3)

        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(ShowCreation(axes), run_time=2)
        self.play(Write(label_x), run_time=1)
        self.play(Write(label_y), run_time=1)
        self.play(Indicate(axes, color=YELLOW), run_time=2)
        self.wait(2)

        # ── Act 2: Plotting a Simple Curve ───────────────
        curve = axes.get_graph(lambda x: x**2, x_range=(-2, 2), color=BLUE)
        curve.set_stroke(width=3)
        self.play(ShowCreation(curve), run_time=3)
        self.play(Indicate(curve, color=YELLOW), run_time=1)
        self.wait(4)

        # ── Act 3: What is "Area Under the Curve"? ───────────────
        shaded_region = axes.get_area_under_graph(curve, x_range=(-1, 1), fill_color=GREEN, fill_opacity=0.3)
        label_area = Text("Area", font_size=30, color=WHITE)
        label_pos = axes.c2p(0, 0.5)
        if label_pos[1] < -3.5:
            label_area.next_to(axes.c2p(0, 0), DOWN, buff=0.5)
        else:
            label_area.next_to(axes.c2p(0, 0.5), DOWN, buff=0.5)

        self.play(FadeIn(shaded_region), run_time=2)
        self.play(Write(label_area), run_time=2)
        self.play(Indicate(shaded_region, color=YELLOW), run_time=1)
        self.wait(4)

        # ── Act 4: Intuition with Rectangles ───────────────
        rectangles = axes.get_riemann_rectangles(curve, x_range=(-1, 1), dx=0.333, input_sample_type="left", colors=[YELLOW], fill_opacity=0.8)
        self.play(LaggedStartMap(ShowCreation, rectangles), run_time=3)
        self.play(Indicate(rectangles[0]), run_time=0.7)
        self.play(Indicate(rectangles[-1]), run_time=0.7)
        self.wait(1.5)
        self.play(Wiggle(rectangles[2]), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(rectangles), run_time=1)

        # ── Act 5: Refining the Approximation ───────────────
        fine_rectangles = axes.get_riemann_rectangles(curve, x_range=(-1, 1), dx=0.166, input_sample_type="left", colors=[YELLOW], fill_opacity=0.8)
        self.play(LaggedStartMap(ShowCreation, fine_rectangles), run_time=3)
        self.wait(1)  # Short pause to let viewer notice the thinner rectangles
        label = Text("More rectangles = Better estimate", font_size=30, color=WHITE)
        label.next_to(curve, UP, buff=0.5)
        self.play(Write(label), run_time=1)
        self.wait(4)  # Remaining time for narrator to explain the improved approximation
        self.play(FadeOut(fine_rectangles), FadeOut(label), run_time=1)

        # ── Act 6: The True Area Concept ───────────────
        exact_area_text = Text("Exact Area = Limit of Rectangles", font_size=30, color=WHITE)
        exact_area_text.move_to(curve.get_center() + UP * 0.5)
        if exact_area_text.get_top()[1] > 3.5:
            exact_area_text.shift(DOWN * (exact_area_text.get_top()[1] - 3.5))

        self.play(Write(exact_area_text), run_time=3)
        self.play(Indicate(exact_area_text, color=YELLOW), run_time=1)
        self.wait(4)
        self.play(FadeOut(exact_area_text), run_time=1)

        # ── Act 7: Closing ───────────────
        closing_message = Text("Area Under the Curve:\nThe Foundation of Integration", font_size=44, color=WHITE)
        closing_message.move_to(ORIGIN)

        self.play(FadeIn(closing_message, scale=0.9), run_time=1)
        self.play(Indicate(closing_message, color=YELLOW), run_time=1)
        self.wait(3)  # Extended wait for pedagogical impact

        # Ensure all objects are still on scene from prior acts; if not, exclude from FadeOut
        self.play(FadeOut(closing_message), run_time=1)
        self.play(
            FadeOut(self.axes) if hasattr(self, 'axes') else AnimationGroup(),
            FadeOut(self.curve) if hasattr(self, 'curve') else AnimationGroup(),
            run_time=1
        )
        self.play(
            FadeOut(self.shaded_region) if hasattr(self, 'shaded_region') else AnimationGroup(),
            FadeOut(self.label_area) if hasattr(self, 'label_area') else AnimationGroup(),
            run_time=1
        )
        self.play(
            FadeOut(self.label_x) if hasattr(self, 'label_x') else AnimationGroup(),
            FadeOut(self.label_y) if hasattr(self, 'label_y') else AnimationGroup(),
            run_time=1
        )
