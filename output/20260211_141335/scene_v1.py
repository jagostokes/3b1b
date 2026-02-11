from manimlib import *

class GeneratedScene(Scene):
    def construct(self):
        # ── Scene 1: Introduction to Neural Networks (~8s) ─────────────────────────
        title = Text("Neural Networks", font_size=48, color=WHITE)
        title.move_to(np.array([0, 3.2, 0]))  # Exact position as per plan
        intro_text = Text("A model inspired by the brain", font_size=36, color=WHITE)
        intro_text.move_to(ORIGIN)

        self.play(FadeIn(title, shift=UP * 0.3), run_time=1.5)
        self.play(FadeIn(intro_text, shift=UP * 0.3), run_time=1.5)
        self.wait(2.0)  # Narrator: "Neural networks are computational models inspired by the human brain."
        self.wait(3.0)  # Narrator: "They process inputs to produce outputs through layers of connected nodes."
        self.wait(0.5)  # Breathing space between scenes
        # Scene 1 total: 8.5s

        # ── Scene 2: Input Layer (~7s) ──────────────────────────
        input_dots = VGroup(
            Dot(np.array([-2, 1, 0]), radius=0.2, color=BLUE),
            Dot(np.array([-2, 0, 0]), radius=0.2, color=BLUE),
            Dot(np.array([-2, -1, 0]), radius=0.2, color=BLUE)
        )
        input_label = Text("Input Layer", font_size=32, color=WHITE)
        input_label.move_to(np.array([-4, 0, 0]))

        self.play(FadeIn(input_dots, shift=LEFT * 0.3), run_time=1.5)
        self.play(FadeIn(input_label, shift=LEFT * 0.3), run_time=1.0)
        self.wait(2.0)  # Narrator: "Data starts at the input layer, represented as nodes."
        self.wait(2.5)  # Narrator: "Each node holds a piece of information, like a pixel value or feature."
        self.wait(0.5)  # Breathing space between scenes
        # Scene 2 total: 7.5s

        # ── Scene 3: Hidden Layer and Connections (~8s) ──────────────────────────
        hidden_dots = VGroup(
            Dot(np.array([0, 1.5, 0]), radius=0.2, color=BLUE),
            Dot(np.array([0, 0.5, 0]), radius=0.2, color=BLUE),
            Dot(np.array([0, -0.5, 0]), radius=0.2, color=BLUE),
            Dot(np.array([0, -1.5, 0]), radius=0.2, color=BLUE)
        )
        hidden_label = Text("Hidden Layer", font_size=32, color=WHITE)
        hidden_label.move_to(np.array([-4, 0, 0]))
        connections1 = VGroup()
        for input_dot in input_dots:
            for hidden_dot in hidden_dots:
                line = Line(input_dot.get_center(), hidden_dot.get_center(), stroke_width=1, color=GREY_A)
                connections1.add(line)

        self.play(FadeIn(hidden_dots, shift=RIGHT * 0.3), run_time=1.5)
        self.play(FadeTransform(input_label, hidden_label), run_time=1.0)
        self.play(ShowCreation(connections1), run_time=1.5)
        self.wait(2.0)  # Narrator: "Inputs connect to a hidden layer, where processing happens."
        self.wait(2.0)  # Narrator: "Each connection has a weight, adjusting the signal strength."
        self.wait(0.5)  # Breathing space between scenes
        # Scene 3 total: 8.5s

        # ── Scene 4: Output Layer and Connections (~8s) ──────────────────────────
        output_dots = VGroup(
            Dot(np.array([2, 0.5, 0]), radius=0.2, color=GREEN),
            Dot(np.array([2, -0.5, 0]), radius=0.2, color=GREEN)
        )
        output_label = Text("Output Layer", font_size=32, color=WHITE)
        output_label.move_to(np.array([4, 0, 0]))
        connections2 = VGroup()
        for hidden_dot in hidden_dots:
            for output_dot in output_dots:
                line = Line(hidden_dot.get_center(), output_dot.get_center(), stroke_width=1, color=GREY_A)
                connections2.add(line)

        self.play(FadeIn(output_dots, shift=RIGHT * 0.3), run_time=1.5)
        self.play(FadeIn(output_label, shift=RIGHT * 0.3), run_time=1.0)
        self.play(ShowCreation(connections2), run_time=1.5)
        self.wait(2.0)  # Narrator: "Hidden layers connect to the output layer, giving results."
        self.wait(2.0)  # Narrator: "Outputs might represent predictions, like a category or value."
        self.wait(0.5)  # Breathing space between scenes
        # Scene 4 total: 8.5s

        # ── Scene 5: Highlighting Flow (~7s) ──────────────────────────
        flow_arrow1 = Arrow(np.array([-2, 0, 0]), np.array([0, 0, 0]), color=YELLOW)
        flow_arrow2 = Arrow(np.array([0, 0, 0]), np.array([2, 0, 0]), color=YELLOW)

        self.play(GrowArrow(flow_arrow1), run_time=1.5)
        self.play(GrowArrow(flow_arrow2), run_time=1.5)
        self.wait(2.0)  # Narrator: "Data flows from input to output through the network."
        self.wait(2.0)  # Narrator: "Learning adjusts weights to improve predictions."
        # Scene 5 total: 7.0s

        # ── Closing (~2s) ────────────────────────────────
        all_objects = VGroup(input_dots, hidden_dots, output_dots, connections1, connections2, hidden_label, output_label, flow_arrow1, flow_arrow2, title)
        summary = Text("Neural Networks: Mimicking the Brain", font_size=44, color=WHITE)
        summary.move_to(ORIGIN)

        self.play(FadeOut(all_objects), run_time=0.5)
        self.play(FadeIn(summary), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(summary), run_time=0.5)
        # Closing total: 2.0s

# TIMING VERIFICATION:
# Scene 1: 8.5s | Scene 2: 7.5s | Scene 3: 8.5s | Scene 4: 8.5s | Scene 5: 7.0s | Closing: 2.0s
# Total: 42.0s