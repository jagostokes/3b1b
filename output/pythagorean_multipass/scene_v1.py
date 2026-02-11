from manimlib import *

class GeneratedScene(Scene):
    def construct(self):

        # ── Act 1: Introducing the Right Triangle ───────────────

        def midpoint(p1, p2):
            return (p1 + p2) / 2

        # Define triangle vertices
        A = np.array([0, 0, 0])  # Right angle vertex
        B = np.array([3, 0, 0])  # Base vertex
        C = np.array([0, 2, 0])  # Height vertex

        # Create the right triangle
        triangle = Polygon(A, B, C, color=WHITE, fill_opacity=0.2)

        # Position the triangle within the safe zone
        triangle.move_to(ORIGIN)

        # Create the right angle marker dynamically
        vec_AB = B - A
        vec_AC = C - A
        marker_pos = A + (normalize(vec_AB) + normalize(vec_AC)) * 0.15
        right_angle_marker = Square(side_length=0.3, color=WHITE)
        right_angle_marker.move_to(marker_pos)

        # Create side labels with consistent colors and dynamic positioning
        label_a = Text("a", font_size=30, color=BLUE).next_to(midpoint(B, C), RIGHT, buff=0.4)
        label_b = Text("b", font_size=30, color=GREEN).next_to(midpoint(A, B), DOWN, buff=0.4)
        label_c = Text("c", font_size=30, color=RED).next_to(midpoint(A, C), LEFT, buff=0.4)

        # Animation sequence
        self.play(ShowCreation(triangle), run_time=1.5)
        self.wait(0.5)
        self.play(ShowCreation(right_angle_marker), run_time=0.5)
        self.play(Indicate(right_angle_marker, color=YELLOW), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(label_a), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(label_b), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(label_c), run_time=1)
        self.wait(0.5)
        self.play(Indicate(label_a, color=BLUE), Indicate(label_b, color=GREEN), Indicate(label_c, color=RED), run_time=1.5)
        self.wait(1)

        # ── Act 2: Square on Side 'a' ───────────────
        # Calculate side 'a' vector (from B to C)
        side_a_vec = C - B

        # Compute perpendicular vector for side 'a' to build the square outward
        perp_a = rotate_vector(side_a_vec, PI/2)
        perp_a = perp_a / np.linalg.norm(perp_a) * np.linalg.norm(side_a_vec)

        # Define square vertices for side 'a'
        D_a = B + perp_a
        E_a = C + perp_a

        # Check if vertices are within screen bounds
        if any(abs(coord) > 7 for coord in D_a[:2]) or any(abs(coord) > 4 for coord in D_a[2:]) or \
           any(abs(coord) > 7 for coord in E_a[:2]) or any(abs(coord) > 4 for coord in E_a[2:]):
            print("Warning: Square vertices D_a or E_a may be off-screen!")

        # Create square for side 'a' with blue outline
        square_a = Polygon(B, C, E_a, D_a, color=BLUE, stroke_width=2, fill_opacity=0.1)

        # Create label for square 'a'
        square_a_label = Text("a²", font_size=24, color=BLUE).move_to(square_a.get_center())
        square_bounds = square_a.get_bounding_box()
        if np.linalg.norm(square_bounds[1] - square_bounds[0]) < 1:  # If square is small
            square_a_label.scale(0.8)

        # Animation sequence for side 'a' square
        self.play(ShowCreation(square_a), run_time=1.5)
        self.wait(1)
        self.play(Indicate(square_a, color=BLUE), run_time=1)
        self.wait(2)
        self.wait(1)
        self.play(FadeIn(square_a_label), run_time=1)
        self.play(square_a_label.animate.scale(1.2).scale(1/1.2), run_time=0.5)
        self.wait(1)

        # ── Act 3: Squares on Sides 'b' and 'c' ───────────────
        # Calculate side 'b' vector (from C to A)
        side_b_vec = A - C

        # Compute perpendicular vector for side 'b' to build the square outward
        perp_b = rotate_vector(side_b_vec, PI/2)
        perp_b = perp_b / np.linalg.norm(perp_b) * np.linalg.norm(side_b_vec)

        # Check orientation using triangle center to ensure outward direction
        triangle_center = (A + B + C) / 3
        if np.dot(perp_b, triangle_center - C) > 0:
            perp_b = -perp_b

        # Define square vertices for side 'b'
        D_b = C + perp_b
        E_b = A + perp_b

        # Check if vertices are within screen bounds
        if any(abs(coord) > 6 for coord in D_b[:2]) or any(abs(coord) > 4 for coord in D_b[2:]) or \
           any(abs(coord) > 6 for coord in E_b[:2]) or any(abs(coord) > 4 for coord in E_b[2:]):
            # Scale down the entire configuration if needed
            scaling_factor = 0.8
            A *= scaling_factor
            B *= scaling_factor
            C *= scaling_factor
            D_a *= scaling_factor
            E_a *= scaling_factor
            D_b *= scaling_factor
            E_b *= scaling_factor
            square_a = Polygon(B, C, E_a, D_a, color=BLUE, stroke_width=2, fill_opacity=0.1)
            square_a_label.move_to(square_a.get_center())

        # Create square for side 'b' with green outline
        square_b = Polygon(C, A, E_b, D_b, color=GREEN, stroke_width=2, fill_opacity=0.1)

        # Create label for square 'b'
        square_b_label = Text("b²", font_size=24, color=GREEN)
        square_bounds_b = square_b.get_bounding_box()
        if np.linalg.norm(square_bounds_b[1] - square_bounds_b[0]) < 1.5:
            square_b_label.scale(0.7).next_to(square_b, UP, buff=0.1)
        else:
            square_b_label.move_to(square_b.get_center())

        # Animation sequence for side 'b' square
        self.play(DrawBorderThenFill(square_b), run_time=1.5)
        self.wait(1)
        self.play(Indicate(square_b, color=GREEN), run_time=1)
        self.wait(1)
        self.play(FadeIn(square_b_label), run_time=1)
        self.wait(1)

        # Calculate side 'c' vector (from A to B)
        side_c_vec = B - A

        # Compute perpendicular vector for side 'c' to build the square outward
        perp_c = rotate_vector(side_c_vec, PI/2)
        perp_c = perp_c / np.linalg.norm(perp_c) * np.linalg.norm(side_c_vec)

        # Check orientation to ensure outward direction
        if np.dot(perp_c, triangle_center - A) > 0:
            perp_c = -perp_c

        # Define square vertices for side 'c'
        D_c = A + perp_c
        E_c = B + perp_c

        # Check if vertices are within screen bounds
        if any(abs(coord) > 6 for coord in D_c[:2]) or any(abs(coord) > 4 for coord in D_c[2:]) or \
           any(abs(coord) > 6 for coord in E_c[:2]) or any(abs(coord) > 4 for coord in E_c[2:]):
            # Scale down the entire configuration if needed
            scaling_factor = 0.8
            A *= scaling_factor
            B *= scaling_factor
            C *= scaling_factor
            D_a *= scaling_factor
            E_a *= scaling_factor
            D_b *= scaling_factor
            E_b *= scaling_factor
            D_c *= scaling_factor
            E_c *= scaling_factor
            square_a = Polygon(B, C, E_a, D_a, color=BLUE, stroke_width=2, fill_opacity=0.1)
            square_b = Polygon(C, A, E_b, D_b, color=GREEN, stroke_width=2, fill_opacity=0.1)
            square_a_label.move_to(square_a.get_center())
            square_b_label.move_to(square_b.get_center())

        # Create square for side 'c' with red outline
        square_c = Polygon(A, B, E_c, D_c, color=RED, stroke_width=2, fill_opacity=0.1)

        # Create label for square 'c'
        square_c_label = Text("c²", font_size=24, color=RED)
        square_bounds_c = square_c.get_bounding_box()
        if np.linalg.norm(square_bounds_c[1] - square_bounds_c[0]) < 1.5:
            square_c_label.scale(0.7).next_to(square_c, UP, buff=0.1)
        else:
            square_c_label.move_to(square_c.get_center())

        # Animation sequence for side 'c' square
        self.play(DrawBorderThenFill(square_c), run_time=1.5)
        self.wait(1)
        self.play(Indicate(square_c, color=RED), run_time=1)
        self.wait(1)
        self.play(FadeIn(square_c_label), run_time=1)
        self.wait(2)

        # Final view with all three squares together
        self.play(Indicate(square_a, color=BLUE), Indicate(square_b, color=GREEN), Indicate(square_c, color=RED), run_time=1.5)
        self.wait(2)

        # ── Act 4: Demonstrating the Theorem ───────────────
        # Create the equation with colored terms to match the squares
        a_term = Text("a²", font_size=36, color=BLUE)
        b_term = Text("b²", font_size=36, color=GREEN)
        c_term = Text("c²", font_size=36, color=RED)
        plus = Text("+", font_size=36, color=WHITE)
        equals = Text("=", font_size=36, color=WHITE)
        equation = VGroup(a_term, plus, b_term, equals, c_term).arrange(RIGHT, buff=0.2)
        equation.next_to(Polygon(A, B, C), DOWN, buff=0.75)

        # Ensure equation stays within screen bounds
        if equation.get_bottom()[1] < -3.5:
            equation.shift(UP * (-3.5 - equation.get_bottom()[1]))

        # Get precise positions for each term
        a_term_pos = a_term.get_center()
        b_term_pos = b_term.get_center()
        c_term_pos = c_term.get_center()

        # Highlight squares a and b together, then point to square c
        self.play(Indicate(square_a, color=BLUE), Indicate(square_b, color=GREEN), run_time=1.5)
        self.wait(1)
        self.play(Indicate(square_c, color=RED), run_time=1.5)
        self.wait(1)

        # Reveal the equation
        self.play(FadeIn(equation), run_time=1.5)
        self.wait(1)

        # Create arrows to connect squares to their respective terms in the equation
        arrow_a = Arrow(square_a.get_center(), a_term_pos, color=BLUE, buff=0.1)
        arrow_b = Arrow(square_b.get_center(), b_term_pos, color=GREEN, buff=0.1)
        arrow_c = Arrow(square_c.get_center(), c_term_pos, color=RED, buff=0.1)

        # Animate connection from square_a to a² term
        self.play(ShowCreation(arrow_a), Indicate(square_a, color=BLUE), run_time=1.2)
        self.wait(1)
        self.play(FadeOut(arrow_a), run_time=0.5)

        # Animate connection from square_b to b² term
        self.play(ShowCreation(arrow_b), Indicate(square_b, color=GREEN), run_time=1.2)
        self.wait(1)
        self.play(FadeOut(arrow_b), run_time=0.5)

        # Animate connection from square_c to c² term
        self.play(ShowCreation(arrow_c), Indicate(square_c, color=RED), run_time=1.2)
        self.wait(1)
        self.play(FadeOut(arrow_c), run_time=0.5)

        # Final emphasis on the entire equation with synchronized square highlights
        self.play(
            Indicate(a_term, color=BLUE), Indicate(square_a, color=BLUE),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            Indicate(b_term, color=GREEN), Indicate(square_b, color=GREEN),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            Indicate(c_term, color=RED), Indicate(square_c, color=RED),
            run_time=1.5
        )
        self.wait(5)  # Hold the final frame to let the viewer process the connection

        # ── Act 5: Closing ───────────────
        # Final message display with emphasis and proper positioning
        final_message = Text("Pythagorean Theorem: a² + b² = c²", font_size=36, color=YELLOW)
        final_message.move_to(DOWN * 3.2)  # Explicitly within safe vertical bounds

        # Fade out existing elements to avoid overlap and ensure focus on final message
        self.play(FadeOut(equation), FadeOut(square_a), FadeOut(square_b), FadeOut(square_c), run_time=1.5)
        self.wait(0.5)

        # Write the final message with emphasis
        self.play(Write(final_message), run_time=2)
        self.play(Indicate(final_message, color=YELLOW), run_time=1.5)
        self.wait(3)  # Extended wait for viewer to process the conclusion
