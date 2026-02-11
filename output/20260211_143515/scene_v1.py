from manimlib import *

class GeneratedScene(Scene):
    def construct(self):

        # ── Act 1: Introduction to the Problem ───────────────
        title = Text("What is the area under this curve?", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2)
        self.wait(1.5)
        self.play(Indicate(title, color=YELLOW), run_time=1)

        axes = Axes(
            x_range=(-3, 3, 1),
            y_range=(-1, 5, 1),
            width=8,
            height=4.5,
            axis_config={"stroke_color": GREY_A}
        )
        axes.shift(0.5 * DOWN)
        self.play(ShowCreation(axes), run_time=1.5)

        graph = axes.get_graph(lambda x: x**2, x_range=(-2, 2), color=BLUE)
        graph.set_stroke(width=3)
        self.play(ShowCreation(graph), run_time=2)
        self.wait(2)

        self.play(FadeOut(title), run_time=0.8)

        # ── Act 2: Dividing into Rectangles ───────────────
        # Act 2: Dividing into Rectangles
        # Create 6 rectangles for coarse approximation of area under y=x² from x=-2 to x=2
        rects_coarse = axes.get_riemann_rectangles(
            graph,
            x_range=(-2, 2),
            dx=0.66,  # Width for 6 rectangles over x=-2 to x=2
            input_sample_type="left",  # Use left endpoint for height
            stroke_width=1,
            stroke_color=BLACK,
            fill_opacity=0.5,
            colors=(YELLOW,),
            negative_color=RED
        )
        # Ensure graph y-values are within [-4, 4] for rectangles to stay in frame bounds

        # Split into two groups to avoid overwhelming the viewer (limit of 5-7 elements)
        rects_coarse_group1 = VGroup(*rects_coarse[:3])
        rects_coarse_group2 = VGroup(*rects_coarse[3:])

        # Animate the two groups sequentially to build the approximation gradually
        self.play(DrawBorderThenFill(rects_coarse_group1, lag_ratio=0.5), run_time=2)
        self.play(DrawBorderThenFill(rects_coarse_group2, lag_ratio=0.5), run_time=2)
        self.wait(1.5)  # Pause for narrator to explain the concept of approximation
        self.play(Indicate(rects_coarse, color=RED), run_time=2.5)
        self.wait(2.0)  # Extra pause to emphasize the key insight of area approximation

        # Cleanup: Fade out rectangles, keep axes and graph for next act
        self.play(FadeOut(rects_coarse), run_time=1)
        self.wait(0.5)

        # ── Act 3: Refining the Approximation ───────────────
        # Create 12 thinner rectangles for a finer approximation of area under y=x² from x=-2 to x=2
        rects_fine = axes.get_riemann_rectangles(
            graph,
            x_range=(-2, 2),
            dx=0.33,  # Width for 12 rectangles over x=-2 to x=2
            input_sample_type="left",  # Use left endpoint for height
            stroke_width=1,
            stroke_color=BLACK,
            fill_opacity=0.5,
            colors=(YELLOW,),
            negative_color=RED
        )

        # Split into three groups to manage cognitive load (limit of 5-7 elements per animation)
        rects_fine_group1 = VGroup(*rects_fine[:4])
        rects_fine_group2 = VGroup(*rects_fine[4:8])
        rects_fine_group3 = VGroup(*rects_fine[8:])

        # Animate the three groups sequentially with short waits to build the approximation gradually
        self.play(DrawBorderThenFill(rects_fine_group1, lag_ratio=0.3), run_time=1.5)
        self.wait(0.5)
        self.play(DrawBorderThenFill(rects_fine_group2, lag_ratio=0.3), run_time=1.5)
        self.wait(0.5)
        self.play(DrawBorderThenFill(rects_fine_group3, lag_ratio=0.3), run_time=1.0)
        self.wait(1.5)  # Pause for narrator to explain the improved approximation
        self.play(Indicate(rects_fine, color=RED), run_time=1.5)  # Reduced from 2.5s to manage total duration
        self.wait(1.0)  # Extra pause to emphasize the key insight

        # Cleanup: Fade out rectangles, keep axes and graph for next act
        self.play(FadeOut(rects_fine), run_time=1)
        self.wait(0.5)

        # ── Act 4: Concept of Limit ───────────────
        # Create text to introduce the concept of limit with infinitely many rectangles
        limit_text = TextMobject("As rectangles → ∞, approximation → exact area", color=WHITE).scale(0.8)
        limit_text.to_edge(UP, buff=0.5)  # Ensure text fits within y=4

        # Create 16 very thin rectangles for an even finer approximation (reduced from 24 to manage cognitive load)
        rects_limit = axes.get_riemann_rectangles(
            graph,
            x_range=(-2, 2),
            dx=0.25,  # Width for 16 rectangles over x=-2 to x=2
            input_sample_type="left",
            stroke_width=0.5,
            stroke_color=BLACK,
            fill_opacity=0.3,
            colors=(YELLOW,),
            negative_color=RED
        )

        # Split into four groups to manage cognitive load (limit of 5-7 elements per animation)
        rects_limit_group1 = VGroup(*rects_limit[:4])
        rects_limit_group2 = VGroup(*rects_limit[4:8])
        rects_limit_group3 = VGroup(*rects_limit[8:12])
        rects_limit_group4 = VGroup(*rects_limit[12:])

        # Animate the text and rectangles with appropriate timing
        self.play(Write(limit_text), run_time=2.0)
        self.wait(1.5)  # Pause for narrator to read the text
        self.play(Indicate(limit_text, color=YELLOW), run_time=1.0)  # Emphasize the key insight
        self.play(DrawBorderThenFill(rects_limit_group1, lag_ratio=0.3), run_time=1.0)
        self.play(DrawBorderThenFill(rects_limit_group2, lag_ratio=0.3), run_time=1.0)
        self.play(DrawBorderThenFill(rects_limit_group3, lag_ratio=0.3), run_time=0.75)
        self.play(DrawBorderThenFill(rects_limit_group4, lag_ratio=0.3), run_time=0.75)
        self.wait(0.5)  # Brief pause to observe the finer approximation

        # Cleanup: Fade out rectangles and text, keep axes and graph for next act
        self.play(FadeOut(rects_limit), FadeOut(limit_text), run_time=1.0)
        self.wait(0.5)

        # ── Act 5: Introducing the Integral ───────────────
        integral_title = Text("This area is the Integral", font_size=40, color=WHITE)
        integral_title.to_edge(UP, buff=0.5)

        integral_symbol = Text("∫ f(x) dx", font_size=40, color=WHITE)
        integral_symbol.next_to(integral_title, DOWN, buff=0.5)

        self.play(Write(integral_title), run_time=2.0)
        self.wait(1.5)
        self.play(Write(integral_symbol), run_time=2.0)
        self.play(Indicate(integral_symbol, color=YELLOW), run_time=1.0)
        self.wait(3.5)

        self.play(FadeOut(integral_title), FadeOut(integral_symbol), run_time=1.0)
        self.wait(0.5)

        # ── Act 6: Closing ───────────────
        closing_message = Text("The Integral = Area Under the Curve", font_size=44, color=WHITE)
        closing_message.move_to(ORIGIN)

        self.play(Write(closing_message), run_time=2.0)
        self.wait(3.0)
        self.play(Indicate(closing_message, color=YELLOW), run_time=1.0)
        self.play(FadeOut(closing_message), FadeOut(axes), FadeOut(graph), run_time=1.0)
