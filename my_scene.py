from manimlib import *


class DerivativeScene(Scene):
    def construct(self):
        # ── Act 1: The Function (~10s) ──────────────────────────────
        title = Text("Derivatives", font_size=60)
        self.play(FadeIn(title, scale=0.8), run_time=1)
        self.wait(0.5)
        self.play(title.animate.scale(0.5).to_edge(UP), run_time=0.8)

        # Axes
        axes = Axes(
            x_range=(-3, 4, 1),
            y_range=(-1, 10, 2),
            width=10,
            height=6,
        )
        axes.shift(0.5 * DOWN)
        axes.add_coordinate_labels(font_size=18)

        # f(x) = x²
        func = lambda x: x ** 2
        graph = axes.get_graph(func, x_range=(-3, 3.3), color=BLUE)
        graph.set_stroke(width=3)

        func_label = Text("f(x) = x\u00b2", font_size=30, color=BLUE)
        func_label.next_to(axes.i2gp(2.8, graph), UR, buff=0.15)

        self.play(ShowCreation(axes), run_time=1.5)
        self.play(ShowCreation(graph), run_time=1.5)
        self.play(FadeIn(func_label, shift=UP * 0.3), run_time=0.8)
        self.wait(0.3)

        # ── Act 2: What Is a Derivative? (~15s) ─────────────────────
        x0 = 1.0
        h_val = 2.0  # initial gap for secant

        dot_a = Dot(axes.i2gp(x0, graph), color=YELLOW, radius=0.07)
        dot_b = Dot(axes.i2gp(x0 + h_val, graph), color=YELLOW, radius=0.07)

        secant = Line(
            axes.i2gp(x0 - 0.5, graph),
            axes.i2gp(x0 + h_val + 0.5, graph),
            color=RED,
        )
        # Extend the secant visually by using the slope
        def build_secant(x_start, x_end):
            p0 = axes.i2gp(x_start, graph)
            p1 = axes.i2gp(x_end, graph)
            direction = normalize(p1 - p0)
            return Line(p0 - direction * 1.2, p1 + direction * 1.2, color=RED)

        secant = build_secant(x0, x0 + h_val)

        delta_label = Text("\u0394y/\u0394x", font_size=26, color=RED)
        delta_label.next_to(secant.get_center(), UR, buff=0.2)

        self.play(FadeIn(dot_a, scale=0.5), FadeIn(dot_b, scale=0.5), run_time=0.6)
        self.play(ShowCreation(secant), run_time=0.8)
        self.play(FadeIn(delta_label, shift=UP * 0.2), run_time=0.6)
        self.wait(0.5)

        # Animate h shrinking: secant → tangent
        h_tracker = ValueTracker(h_val)

        def secant_updater(line):
            h = h_tracker.get_value()
            xa, xb = x0, x0 + h
            pa = axes.i2gp(xa, graph)
            pb = axes.i2gp(xb, graph)
            direction = normalize(pb - pa)
            line.put_start_and_end_on(
                pa - direction * 1.5,
                pb + direction * 1.5,
            )

        secant.add_updater(secant_updater)
        dot_b.add_updater(
            lambda d: d.move_to(axes.i2gp(x0 + h_tracker.get_value(), graph))
        )
        delta_label.add_updater(lambda l: l.next_to(secant.get_center(), UR, buff=0.2))

        self.play(h_tracker.animate.set_value(0.01), run_time=3, rate_func=smooth)
        self.wait(0.3)

        # Swap label
        deriv_label = Text("dy/dx", font_size=26, color=GREEN)
        deriv_label.move_to(delta_label)
        self.play(FadeTransform(delta_label, deriv_label), run_time=0.8)

        # Clean up secant updaters, replace with a proper tangent
        secant.clear_updaters()
        dot_b.clear_updaters()

        tangent = axes.get_tangent_line(x0, graph, length=4)
        tangent.set_color(GREEN)
        self.play(
            ReplacementTransform(secant, tangent),
            FadeOut(dot_b),
            run_time=0.8,
        )
        self.wait(0.5)

        # ── Act 3: Moving Tangent Line (~15s) ───────────────────────
        self.play(FadeOut(deriv_label), run_time=0.4)

        x_tracker = ValueTracker(x0)

        # Slope display in upper-right
        slope_label = Text("slope = ", font_size=28, color=GREEN)
        slope_num = DecimalNumber(
            axes.slope_of_tangent(x0, graph),
            num_decimal_places=2,
            font_size=28,
            color=GREEN,
        )
        slope_group = VGroup(slope_label, slope_num).arrange(RIGHT, buff=0.1)
        slope_group.to_corner(UR, buff=0.5)

        # Updaters
        dot_a.add_updater(
            lambda d: d.move_to(axes.i2gp(x_tracker.get_value(), graph))
        )
        tangent.add_updater(
            lambda t: t.become(
                axes.get_tangent_line(x_tracker.get_value(), graph, length=4)
                .set_color(GREEN)
            )
        )
        slope_num.add_updater(
            lambda s: s.set_value(axes.slope_of_tangent(x_tracker.get_value(), graph))
        )

        self.play(FadeIn(slope_group), run_time=0.5)

        # Sweep the tangent line across the curve
        self.play(x_tracker.animate.set_value(-2), run_time=2.5, rate_func=smooth)
        self.play(x_tracker.animate.set_value(3), run_time=4, rate_func=smooth)
        self.wait(0.5)

        # ── Act 4: The Derivative Function (~15s) ────────────────────
        dot_a.clear_updaters()
        tangent.clear_updaters()
        slope_num.clear_updaters()

        self.play(
            FadeOut(tangent),
            FadeOut(dot_a),
            FadeOut(slope_group),
            run_time=0.8,
        )

        # Plot f'(x) = 2x
        deriv_func = lambda x: 2 * x
        deriv_graph = axes.get_graph(deriv_func, x_range=(-3, 3.3), color=GREEN)
        deriv_graph.set_stroke(width=3)

        deriv_func_label = Text("f'(x) = 2x", font_size=30, color=GREEN)
        deriv_func_label.next_to(axes.i2gp(3, deriv_graph), RIGHT, buff=0.2)

        self.play(ShowCreation(deriv_graph), run_time=2)
        self.play(FadeIn(deriv_func_label, shift=UP * 0.3), run_time=0.8)
        self.wait(0.5)

        # Highlight connection: vertical lines showing f steep → f' large
        highlight_x_vals = [-2, 0, 2]
        v_lines = VGroup()
        for xv in highlight_x_vals:
            pt_f = axes.i2gp(xv, graph)
            pt_fp = axes.i2gp(xv, deriv_graph)
            vl = DashedLine(pt_f, pt_fp, dash_length=0.08, color=YELLOW)
            v_lines.add(vl)

        self.play(
            LaggedStart(*[ShowCreation(vl) for vl in v_lines], lag_ratio=0.3),
            run_time=2,
        )
        self.wait(1)

        # ── Act 5: Closing (~5s) ────────────────────────────────────
        # Fade everything and show closing message
        all_objs = VGroup(
            axes, graph, func_label, deriv_graph, deriv_func_label,
            v_lines, title,
        )
        closing = Text(
            "The derivative measures\nthe rate of change",
            font_size=44,
        )

        self.play(FadeOut(all_objs), run_time=1)
        self.play(FadeIn(closing, scale=0.9), run_time=1)
        self.wait(2)
        self.play(FadeOut(closing), run_time=1)
