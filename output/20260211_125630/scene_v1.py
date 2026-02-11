from manimlib import *

class GeneratedScene(Scene):
    def construct(self):

        # ── Act 1: Introduction to Composition ───────────────
        comp_text = Text("f(g(x))", color=BLUE)
        comp_text.scale(1.5)
        comp_text.move_to(ORIGIN)

        inner_text = Text("g(x)", color=YELLOW)
        inner_text.scale(1.0)
        inner_text.next_to(comp_text, DOWN, buff=0.5)

        outer_text = Text("f( )", color=GREEN)
        outer_text.scale(1.0)
        outer_text.next_to(comp_text, UP, buff=0.5)

        self.play(Write(comp_text), run_time=3)
        self.play(Indicate(comp_text), run_time=1)
        self.wait(1.5)
        self.play(Write(inner_text), run_time=1.5)
        self.play(Write(outer_text), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(VGroup(comp_text, inner_text, outer_text)), run_time=1)

        # ── Act 2: Visualizing Nested Functions ───────────────
        axes = Axes(
            x_range=(-3, 3, 1),
            y_range=(-2, 4, 1),
            width=10,
            height=6,
            axis_config=dict(stroke_color=GREY_A, stroke_width=2)
        )
        axes.shift(0.5 * DOWN)
        axes.add_coordinate_labels(font_size=18)

        graph_g = axes.get_graph(lambda x: x**2, x_range=(-2, 2), color=YELLOW)
        graph_g.set_stroke(width=3)

        graph_f_g = axes.get_graph(lambda x: (x**2)**2, x_range=(-2, 2), color=GREEN)
        graph_f_g.set_stroke(width=3)

        label_g = Text("g(x) = x²", font_size=30, color=YELLOW)
        label_g.next_to(axes.i2gp(1.5, graph_g), RIGHT, buff=0.2)

        label_f_g = Text("f(g(x)) = (x²)²", font_size=30, color=GREEN)
        label_f_g.next_to(axes.i2gp(1.0, graph_f_g), UR, buff=0.3)

        self.play(ShowCreation(axes), run_time=1.5)
        self.play(ShowCreation(graph_g), run_time=1.5)
        self.play(Indicate(graph_g, color=YELLOW), run_time=1)
        self.wait(0.5)  # Brief pause before label
        self.play(Write(label_g), run_time=1)
        self.wait(1.5)  # Time for viewer to process g(x)
        self.play(ShowCreation(graph_f_g), run_time=1.5)
        self.play(Indicate(graph_f_g, color=GREEN), run_time=1)
        self.wait(0.5)  # Brief pause before label
        self.play(Write(label_f_g), run_time=1)
        self.wait(2)  # Extended wait for viewer to process the transformation
        self.play(FadeOut(VGroup(label_g, label_f_g)), run_time=1)  # Keep axes and graphs for next act

        # ── Act 3: Rate of Change for g(x) ───────────────
        dot_g = Dot(axes.i2gp(1, graph_g), color=YELLOW, radius=0.07)
        tangent_g = axes.get_tangent_line(1, graph_g, length=4)
        tangent_g.set_color(YELLOW)
        tangent_g.set_stroke(width=2)

        label_dg = Text("dg/dx", font_size=26, color=YELLOW)
        side_vector = tangent_g.get_end() - tangent_g.get_start()
        perp_direction = normalize(np.array([-side_vector[1], side_vector[0], 0]))
        label_dg.next_to(tangent_g.get_center(), perp_direction, buff=0.3)

        self.play(FadeIn(dot_g, scale=0.5), run_time=1)
        self.play(ShowCreation(tangent_g), run_time=1.5)
        self.play(Indicate(tangent_g, color=YELLOW), run_time=1)
        self.wait(2)  # Extended pause to emphasize the tangent line
        self.play(Write(label_dg), run_time=1.5)
        self.wait(3)  # Extended wait for viewer to connect label to tangent
        self.play(FadeOut(label_dg), run_time=0.5)

        # ── Act 4: Rate of Change for f(g(x)) ───────────────
        dot_f_g = Dot(axes.i2gp(1, graph_f_g), color=GREEN, radius=0.07)
        tangent_f_g = axes.get_tangent_line(1, graph_f_g, length=4)
        tangent_f_g.set_color(GREEN)
        tangent_f_g.set_stroke(width=2)

        label_df = Text("df/dg", font_size=26, color=GREEN)
        side_vector_f = tangent_f_g.get_end() - tangent_f_g.get_start()
        perp_direction_f = normalize(np.array([-side_vector_f[1], side_vector_f[0], 0]))
        label_df.next_to(tangent_f_g.get_center(), perp_direction_f, buff=0.3)

        self.play(FadeIn(dot_f_g, scale=0.5), run_time=1)
        self.play(ShowCreation(tangent_f_g), run_time=1.5)
        self.play(Write(label_df), run_time=1.5)
        self.play(Indicate(label_df, color=WHITE), run_time=1)
        self.wait(3)
        self.play(FadeOut(label_df), run_time=0.5)

        # ── Act 5: Combining Rates of Change ───────────────
        chain_rule_text = Text("df/dx = df/dg \u00d7 dg/dx", font_size=36, color=BLUE)
        chain_rule_text.to_edge(UP, buff=0.3)
        if chain_rule_text.get_y() > 3.5:
            chain_rule_text.scale(0.9)

        arrow_mult = Arrow(
            start=tangent_g.get_center(),
            end=tangent_f_g.get_center(),
            color=RED,
            buff=0.2
        )

        self.play(Write(chain_rule_text), run_time=2)
        self.play(Indicate(chain_rule_text, color=YELLOW), run_time=1.5)
        self.wait(2)
        self.play(ShowCreation(arrow_mult), run_time=1.5)
        self.play(Indicate(arrow_mult, color=YELLOW), run_time=1.5)
        self.wait(1.5)
        self.play(FadeOut(arrow_mult), run_time=0.5)

        # ── Act 6: Closing ───────────────
        # Closing message
        closing_text = Text("Chain Rule: Derivative of composition\nis the product of derivatives", font_size=40, color=WHITE)
        closing_text.move_to(ORIGIN)

        # Group all objects for final cleanup
        all_objects = VGroup(
            *[obj for obj in [axes, graph_g, graph_f_g, dot_g, dot_f_g, tangent_g, tangent_f_g, chain_rule_text, closing_text] if obj in self.mobjects]
        )

        self.play(FadeIn(closing_text, scale=0.9), run_time=1)
        self.wait(3)  # Extended wait for audience to absorb the message
        self.play(Indicate(closing_text, color=YELLOW), run_time=1)
        self.wait(2)  # Additional reflection time after emphasis
        self.play(FadeOut(all_objects), run_time=2)
