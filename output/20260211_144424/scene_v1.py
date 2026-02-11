from manimlib import *

class GeneratedScene(Scene):
    def construct(self):

        # ── Act 1: Introduction to Regression ───────────────
        regression_text = Text("Regression: Predicting a number from inputs", color=WHITE, font_size=48)
        regression_text.shift(UP * 2)
        example_text = Text("e.g., predict house price from size", color=WHITE, font_size=36)
        example_text.shift(UP * 1)

        self.play(Write(regression_text), run_time=2)
        self.wait(1.5)
        self.play(Indicate(regression_text, color=YELLOW), run_time=1)
        self.wait(1.0)
        self.play(Write(example_text), run_time=2)
        self.wait(1.5)

        self.play(FadeOut(regression_text), FadeOut(example_text), run_time=1)

        # ── Act 2: Input and Output Representation ───────────────
        input_dot = Dot(LEFT * 4, color=BLUE, radius=0.08)
        output_dot = Dot(RIGHT * 4, color=GREEN, radius=0.08)
        input_to_output = Arrow(input_dot.get_center(), output_dot.get_center(), color=WHITE, buff=0.1)
        input_label = Text("Input (e.g., size)", color=BLUE, font_size=30)
        input_label.next_to(input_dot, DOWN, buff=0.5)
        output_label = Text("Output (price)", color=GREEN, font_size=30)
        output_label.next_to(output_dot, DOWN, buff=0.5)

        self.play(FadeIn(input_dot, scale=0.5), run_time=1)
        self.play(FadeIn(output_dot, scale=0.5), run_time=1)
        self.play(GrowArrow(input_to_output), run_time=1.5)
        self.play(Indicate(input_to_output, color=YELLOW), run_time=1)
        self.wait(1)
        self.play(Write(input_label), run_time=1.5)
        self.wait(1)
        self.play(Write(output_label), run_time=1.5)
        self.wait(2)

        # ── Act 3: Neural Network Structure ───────────────
        hidden_dots = VGroup(
            Dot(ORIGIN + UP * 1, color=YELLOW, radius=0.08),
            Dot(ORIGIN, color=YELLOW, radius=0.08),
            Dot(ORIGIN + DOWN * 1, color=YELLOW, radius=0.08)
        )

        input_to_hidden = VGroup()
        for h_dot in hidden_dots:
            line = Line(input_dot.get_center(), h_dot.get_center(), color=WHITE)
            input_to_hidden.add(line)

        hidden_to_output = VGroup()
        for h_dot in hidden_dots:
            line = Line(h_dot.get_center(), output_dot.get_center(), color=WHITE)
            hidden_to_output.add(line)

        hidden_label = Text("Hidden Layer", color=YELLOW, font_size=30)
        hidden_label.next_to(hidden_dots, UP, buff=0.5)

        self.play(FadeIn(hidden_dots, scale=0.5), run_time=1.5)
        self.wait(0.5)
        self.play(
            LaggedStart(*[ShowCreation(line) for line in input_to_hidden], lag_ratio=0.2),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            LaggedStart(*[ShowCreation(line) for line in hidden_to_output], lag_ratio=0.2),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(Write(hidden_label), run_time=1.5)
        self.wait(1.5)
        self.play(Indicate(hidden_dots, scale_factor=1.2, color=YELLOW), run_time=1)
        self.wait(0.5)

        # ── Act 4: Weights and Connections ───────────────
        weights_text = Text("Weights adjust influence", color=WHITE, font_size=30)
        weights_text.to_edge(DOWN, buff=0.5)

        weight_brace = Brace(input_to_hidden[0], UP, buff=0.1, color=RED)
        weight_label = Text("w1", color=RED, font_size=24)
        weight_label.next_to(weight_brace, UP, buff=0.2)

        self.play(Write(weights_text), run_time=2)
        self.wait(1.0)
        self.play(FadeIn(weight_brace), run_time=1.5)
        self.play(FadeIn(weight_label), run_time=1.5)
        self.play(Indicate(weight_brace, color=YELLOW), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(weights_text), FadeOut(weight_brace), FadeOut(weight_label), run_time=1)
        self.wait(1.0)

        # ── Act 5: Activation and Prediction ───────────────
        # Act 5: Activation and Prediction
        prediction_text = Text("Prediction!", color=GREEN, font_size=30)
        if output_dot.get_center()[1] > 3:
            prediction_text.move_to(UP * 3)
        else:
            prediction_text.next_to(output_dot, UP, buff=0.5)

        self.play(FlashAround(input_dot, color=BLUE), run_time=1)
        self.wait(1)
        self.play(FlashAround(hidden_dots, color=YELLOW), run_time=1.5)
        self.wait(1)
        self.play(FlashAround(output_dot, color=GREEN), run_time=1.5)
        self.wait(1)
        self.play(Write(prediction_text), run_time=2)
        self.wait(2)
        self.play(Indicate(prediction_text, color=GREEN), run_time=1)
        self.wait(1)

        # ── Act 6: Learning Through Error ───────────────
        error_text = Text("Error = Actual - Predicted", color=WHITE, font_size=30)
        error_text.to_edge(DOWN, buff=1)

        adjust_text = Text("Adjust weights to minimize error", color=WHITE, font_size=30)
        adjust_text.next_to(error_text, UP, buff=0.5)

        error_arrow = Arrow(
            start=output_dot.get_center(),
            end=output_dot.get_bottom() + DOWN * 0.5,
            color=RED,
            buff=0.1
        )

        self.play(Write(error_text), run_time=2)
        self.wait(1)
        self.play(Indicate(error_text, color=YELLOW), run_time=1)
        self.wait(0.5)
        self.play(GrowArrow(error_arrow), run_time=1.5)
        self.wait(1)
        self.play(Write(adjust_text), run_time=2)
        self.wait(2.5)

        self.play(FadeOut(error_text), FadeOut(error_arrow), FadeOut(adjust_text), run_time=1)

        # ── Act 7: Closing ───────────────
        # Closing act: Final message and cleanup
        final_message = Text("Neural Networks learn to predict by adjusting weights!", color=WHITE, font_size=36)
        final_message.shift(UP * 1.5)  # Adjusted to stay within frame bounds

        # Objects from prior acts assumed to be defined
        all_objects = VGroup(input_dot, output_dot, input_to_hidden, hidden_to_output, hidden_dots, hidden_label, prediction_text)

        self.play(FadeOut(all_objects), run_time=1)
        self.play(FadeIn(final_message, scale=0.9), run_time=1.5)
        self.wait(2)
        self.play(Indicate(final_message, color=YELLOW), run_time=1)  # Emphasis on key insight
        self.wait(1)
        self.play(FadeOut(final_message), run_time=1)
