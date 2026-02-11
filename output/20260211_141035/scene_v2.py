from manimlib import *

class GeneratedScene(Scene):
    def construct(self):
        # ── Scene 1: Title Introduction (~4s) ─────────────────────────
        title = Text("Understanding Derivatives", font_size=48, color=WHITE)
        title.move_to(np.array([0, 3.5, 0]))
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1.5)
        self.wait(1.5)
        self.play(title.animate.scale(0.7).move_to(np.array([0, 3.5, 0])), run_time=1.0)
        # Scene 1 total: 4.0s

        # ── Scene 2: Visual Definition - Slope of a Curve (~8s) ──────────────────────────
        axes = Axes(x_range=(-3, 4, 1), y_range=(-2, 10, 2), width=10, height=6)
        axes.shift(0.5 * DOWN)
        axes.add_coordinate_labels(font_size=18)

        func = lambda x: x ** 2
        graph = axes.get_graph(func, x_range=(-3, 3.3), color=BLUE)
        graph.set_stroke(width=3)

        graph_label = Text("f(x) = x\u00b2", font_size=30, color=BLUE)
        graph_label.next_to(axes.i2gp(2.8, graph), UR, buff=0.15)

        self.play(ShowCreation(axes), run_time=1.5)
        self.play(ShowCreation(graph), run_time=2.0)
        self.play(FadeIn(graph_label, shift=RIGHT * 0.2), run_time=1.0)
        self.wait(2.0)
        self.wait(1.5)
        # Scene 2 total: 8.0s

        # ── Scene 3: Geometric Intuition - Secant to Tangent (~9s) ──────────────────────────
        point1 = Dot(axes.i2gp(-1, graph), color=YELLOW, radius=0.1)
        point2 = Dot(axes.i2gp(1, graph), color=YELLOW, radius=0.1)
        secant = Line(point1.get_center(), point2.get_center(), color=RED, stroke_width=2)
        point3 = Dot(axes.i2gp(0, graph), color=YELLOW, radius=0.1)

        def get_tangent_at_x(axes, graph, x_val, length=2.0):
            point = axes.i2gp(x_val, graph)
            derivative = 2 * x_val  # for f(x)=x²
            slope_line = Line(point - LEFT * length/2, point + RIGHT * length/2)
            slope_line.rotate(np.arctan(derivative), about_point=point)
            return slope_line

        tangent = get_tangent_at_x(axes, graph, 0, length=2.0)
        tangent.set_color(GREEN)
        tangent.set_stroke(width=2)

        self.play(FadeIn(point1), FadeIn(point2), run_time=1.0)
        self.play(ShowCreation(secant), run_time=1.5)
        self.wait(2.0)
        self.play(FadeIn(point3), run_time=1.0)
        self.play(ReplacementTransform(secant, tangent), run_time=1.5)
        self.wait(1.5)
        self.play(FadeOut(point1), FadeOut(point2), run_time=0.5)
        # Scene 3 total: 9.0s

        # ── Scene 4: Symbolic Form - Derivative Notation (~8s) ──────────────────────────
        equation = Text("f'(x) = 2x", font_size=36, color=GREEN)
        equation.move_to(np.array([-4, 2.0, 0]))
        label_tangent = Text("slope = 2x", font_size=24, color=GREEN)
        label_tangent.next_to(tangent, UP, buff=0.4)

        self.play(FadeIn(equation, shift=UP * 0.3), run_time=1.5)
        self.wait(2.0)
        self.play(FadeIn(label_tangent, shift=UP * 0.2), run_time=1.0)
        self.wait(2.0)
        self.play(Indicate(equation, color=YELLOW), run_time=1.5)
        # Scene 4 total: 8.0s

        # ── Scene 5: Connect Visual to Symbolic - Slope at a Point (~7s) ──────────────────────────
        value_label = Text("x = 1, slope = 2", font_size=28, color=GREEN)
        value_label.move_to(np.array([-4, 1.0, 0]))
        new_point = Dot(axes.i2gp(1, graph), color=YELLOW, radius=0.1)
        new_tangent = get_tangent_at_x(axes, graph, 1, length=2.0)
        new_tangent.set_color(GREEN)
        new_tangent.set_stroke(width=2)

        self.play(FadeIn(value_label, shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(new_point), run_time=1.0)
        self.play(ShowCreation(new_tangent), run_time=1.5)
        self.wait(2.0)
        self.play(Indicate(new_tangent, color=YELLOW), run_time=1.0)
        self.play(FadeOut(value_label), FadeOut(new_point), FadeOut(new_tangent), run_time=0.5)
        # Scene 5 total: 7.0s

        # ── Closing (~4s) ────────────────────────────────
        all_objects = VGroup(title, axes, graph, graph_label, point3, tangent, equation, label_tangent)
        summary = Text("Derivatives: Slope of the Curve", font_size=44, color=WHITE)
        summary.move_to(ORIGIN)

        self.play(FadeOut(all_objects), run_time=1.0)
        self.play(FadeIn(summary), run_time=1.0)
        self.wait(1.5)
        self.play(FadeOut(summary), run_time=0.5)
        # Closing total: 4.0s