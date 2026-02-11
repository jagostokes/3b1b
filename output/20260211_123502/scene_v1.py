from manimlib import *

class GeneratedScene(Scene):
    def construct(self):
        # ── Act 1: Introduction to Composition (~10s) ─────────────────────────
        title = Text("Understanding the Chain Rule", font_size=60)
        self.play(FadeIn(title, scale=0.8), run_time=1)
        self.wait(1.5)
        self.play(title.animate.scale(0.5).to_edge(UP), run_time=0.8)

        inner_func = Text("g(x)", font_size=40, color=BLUE)
        outer_func = Text("f(u)", font_size=40, color=GREEN)
        composite_func = Text("f(g(x))", font_size=40, color=YELLOW)

        inner_func.to_edge(LEFT, buff=1)
        outer_func.next_to(inner_func, RIGHT, buff=2)
        composite_func.move_to(outer_func.get_center() + RIGHT * 2)

        arrow1 = Arrow(inner_func.get_right(), outer_func.get_left(), buff=0.25, color=WHITE)
        arrow2 = Arrow(outer_func.get_right(), composite_func.get_left(), buff=0.25, color=WHITE)

        self.play(FadeIn(inner_func, shift=RIGHT * 0.3), run_time=0.8)
        self.play(FadeIn(outer_func, shift=RIGHT * 0.3), GrowArrow(arrow1), run_time=0.8)
        self.play(FadeIn(composite_func, shift=RIGHT * 0.3), GrowArrow(arrow2), run_time=0.8)
        self.wait(2)

        act1_objects = VGroup(inner_func, outer_func, composite_func, arrow1, arrow2)
        self.play(FadeOut(act1_objects), run_time=1)
        self.wait(0.5)

        # ── Act 2: Visualizing Nested Functions (~12s) ────────────────────────
        axes = Axes(x_range=(-3, 3, 1), y_range=(-2, 2, 1), width=10, height=6)
        axes.shift(0.5 * DOWN)
        axes.add_coordinate_labels(font_size=18)

        g_func = lambda x: x ** 2
        f_func = lambda u: np.sin(u)
        composite_func_graph = lambda x: np.sin(x ** 2)

        g_graph = axes.get_graph(g_func, x_range=(-1.5, 1.5), color=BLUE)
        g_graph.set_stroke(width=3)
        g_label = Text("g(x) = x²", font_size=30, color=BLUE)
        g_label.next_to(axes.i2gp(1.4, g_graph), UR, buff=0.15)

        composite_graph = axes.get_graph(composite_func_graph, x_range=(-1.8, 1.8), color=YELLOW)
        composite_graph.set_stroke(width=3)
        composite_label = Text("f(g(x)) = sin(x²)", font_size=30, color=YELLOW)
        composite_label.next_to(axes.i2gp(1.7, composite_graph), RIGHT, buff=0.15)

        self.play(ShowCreation(axes), run_time=1.5)
        self.play(ShowCreation(g_graph), FadeIn(g_label, shift=UP * 0.3), run_time=1.5)
        self.wait(1.5)

        f_label = Text("f(u) = sin(u)", font_size=30, color=GREEN)
        f_label.to_corner(UR, buff=0.5)
        self.play(FadeIn(f_label, shift=DOWN * 0.3), run_time=0.8)
        self.wait(1)

        self.play(ShowCreation(composite_graph), FadeIn(composite_label, shift=UP * 0.3), run_time=2)
        self.wait(1.5)

        # ── Act 3: Rates of Change - Inner and Outer (~12s) ───────────────────
        x0 = 1.0
        dot_g = Dot(axes.i2gp(x0, g_graph), color=WHITE, radius=0.07)
        tangent_g = axes.get_tangent_line(x0, g_graph, length=3)
        tangent_g.set_color(BLUE)
        dg_dx_label = Text("dg/dx", font_size=26, color=BLUE)
        dg_dx_label.next_to(tangent_g.get_center(), UR, buff=0.2)

        u0 = g_func(x0)  # u = g(x) = 1² = 1
        f_axes = Axes(x_range=(-2, 2, 1), y_range=(-1.5, 1.5, 1), width=3, height=2)
        f_axes.to_corner(UR, buff=0.5)
        f_graph = f_axes.get_graph(f_func, x_range=(-1.5, 1.5), color=GREEN)
        f_graph.set_stroke(width=2)
        dot_f = Dot(f_axes.i2gp(u0, f_graph), color=WHITE, radius=0.05)
        tangent_f = f_axes.get_tangent_line(u0, f_graph, length=2)
        tangent_f.set_color(GREEN)
        df_du_label = Text("df/du", font_size=20, color=GREEN)
        df_du_label.next_to(tangent_f.get_center(), UR, buff=0.1)

        connection_line = DashedLine(dot_g.get_center(), dot_f.get_center(), color=YELLOW)

        self.play(FadeIn(dot_g, scale=0.5), ShowCreation(tangent_g), run_time=1)
        self.play(FadeIn(dg_dx_label, shift=UP * 0.2), run_time=0.6)
        self.wait(1.5)
        self.play(ShowCreation(f_axes), ShowCreation(f_graph), run_time=1.5)
        self.play(FadeIn(dot_f, scale=0.5), ShowCreation(tangent_f), ShowCreation(connection_line), run_time=1)
        self.play(FadeIn(df_du_label, shift=UP * 0.2), run_time=0.6)
        self.wait(1.5)
        self.play(Indicate(dg_dx_label, color=YELLOW), Indicate(df_du_label, color=YELLOW), run_time=1.5)
        self.wait(1.5)

        # ── Act 4: Chain Rule Formula (~10s) ────────────────────────────────
        chain_rule = Text("df/dx = df/du × dg/dx", font_size=40, color=WHITE)
        chain_rule.to_edge(DOWN, buff=0.5)

        dg_val = 2 * x0  # dg/dx = 2x at x=1 → 2
        df_val = np.cos(u0)  # df/du = cos(u) at u=1
        df_dx_val = df_val * dg_val

        values = Text(f"df/du = cos(1) ≈ {df_val:.2f}", font_size=30, color=GREEN)
        values2 = Text(f"dg/dx = 2 × 1 = {dg_val:.1f}", font_size=30, color=BLUE)
        result = Text(f"df/dx ≈ {df_dx_val:.2f}", font_size=30, color=YELLOW)
        value_group = VGroup(values, values2, result).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        value_group.next_to(chain_rule, UP, buff=0.5)

        self.play(FadeIn(chain_rule, shift=UP * 0.3), run_time=0.8)
        self.wait(1.5)
        self.play(LaggedStart(
            FadeIn(values, shift=RIGHT * 0.3),
            FadeIn(values2, shift=RIGHT * 0.3),
            FadeIn(result, shift=RIGHT * 0.3),
            lag_ratio=0.5
        ), run_time=2.5)
        self.wait(2)
        self.play(Indicate(result, color=YELLOW), run_time=1)
        self.wait(1.5)

        # ── Closing (~6s) ────────────────────────────────────────────────
        all_objs = VGroup(axes, g_graph, g_label, composite_graph, composite_label, f_axes, f_graph, f_label, dot_g, dot_f, tangent_g, tangent_f, dg_dx_label, df_du_label, connection_line, value_group, chain_rule, title)
        closing = Text("Chain Rule:\nDerivative of Composite = Outer' × Inner'", font_size=44)

        self.play(FadeOut(all_objs), run_time=1)
        self.play(FadeIn(closing, scale=0.9), run_time=1)
        self.wait(2)
        self.play(FadeOut(closing), run_time=1)