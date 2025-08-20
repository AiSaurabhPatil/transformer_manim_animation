from manim import *

class MatrixMultiplicationAnimation(Scene):
    def construct(self):
        # Define the two matrices
        
        
        title = Text("Matrix Multiplication", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))
        self.wait(1)
        matrix1_vals = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        matrix2_vals = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]

        # Create Manim Matrix objects
        matrix1 = Matrix(matrix1_vals).scale(0.7)
        matrix2 = Matrix(matrix2_vals).scale(0.7)
        
        matrix1.set_color(RED)
        matrix2.set_color(BLUE)
        # Position the matrices
        matrix1.to_edge(LEFT, buff=2)
        multiply_sign = MathTex(r"\times").scale(1.5)
        multiply_sign.next_to(matrix1, RIGHT, buff=0.4)
        matrix2.next_to(multiply_sign, RIGHT, buff=0.4)

        # Display initial matrices and sign
        self.play(Write(matrix1), Write(matrix2), Write(multiply_sign))
        self.wait(1)

        # Calculate the result matrix
        result_matrix_vals = [
            [sum(a * b for a, b in zip(row, col)) for col in zip(*matrix2_vals)]
            for row in matrix1_vals
        ]
        result_matrix = Matrix(result_matrix_vals).scale(0.8)
        
        # Group the matrices and the sign
        equation = VGroup(matrix1, multiply_sign, matrix2)
        
        # # Animate moving the equation to the top
        # self.play(equation.animate.to_edge(UP, buff=0.5))
        
        # Create an equals sign and position the result matrix
        equals_sign = MathTex("=").next_to(equation, RIGHT, buff=0.5)
        result_matrix.next_to(equals_sign, RIGHT, buff=0.5)
        result_matrix.set_color(GREEN)

        # Animate the appearance of the equals sign and the result matrix structure
        self.play(Write(equals_sign), Write(result_matrix.get_brackets()))
        self.wait(0.5)

        # Animate the calculation of each element in the result matrix
        for i in range(3):  # Row index
            for j in range(3):  # Column index
                # Highlight row from matrix1
                matrix1.set_color(RED)
                matrix2.set_color(BLUE)
                row_to_highlight = matrix1.get_rows()[i]
                
                rowbox = SurroundingRectangle(row_to_highlight, buff = .1 ,corner_radius=0.1)
                self.play(Create(rowbox), run_time=0.5)
                # self.play(row_to_highlight.animate.set_color(YELLOW), run_time=0.3)
                
                # Highlight column from matrix2
                col_to_highlight = matrix2.get_columns()[j]
                
                columbox = SurroundingRectangle(col_to_highlight, buff = .1 ,corner_radius=0.1)
                self.play(Create(columbox), run_time=0.5)
                # self.play(col_to_highlight.animate.set_color(ORANGE), run_time=0.3)
                
                # Create a temporary VGroup for the moving parts
                moving_row = row_to_highlight.copy()
                moving_col = col_to_highlight.copy()
                row_group = VGroup(moving_row, rowbox)
                col_group = VGroup(moving_col, columbox)
                # Animate moving highlighted parts towards the result position
                target_pos = result_matrix.get_entries()[i*3 + j].get_center()
                
                # Show calculation
                row_vals = matrix1_vals[i]
                col_vals = [matrix2_vals[k][j] for k in range(3)]
                calc_str = "+".join([f"{r} \\times {c}" for r, c in zip(row_vals, col_vals)])
                calculation_tex = MathTex(calc_str, font_size=36).move_to(DOWN*2)
                calculation_tex.set_color(GREEN)
                self.play(
                    Transform(row_group, calculation_tex),
                    Transform(col_group, calculation_tex),
                    run_time=0.5
                    
                )
        
                # Show the result of the calculation
                result_val = result_matrix_vals[i][j]
                result_tex = MathTex(str(result_val), font_size=36).move_to(target_pos)
                result_tex.set_color(GREEN)
                self.play(
                    FadeOut(moving_row),
                    FadeOut(moving_col),
                    FadeOut(calculation_tex,),
                    Transform(calculation_tex, result_tex)
                )

                # Replace the placeholder with the final value
                self.play(
                    FadeOut(calculation_tex),
                    Write(result_matrix.get_entries()[i*3 + j].move_to(target_pos))
                )
        # Wait a moment to show the completed calculation
        self.wait(1)
        
        # Create a copy of the result matrix for the final display
        final_result_matrix = result_matrix.copy().scale(1.2).move_to(ORIGIN)
        
        # Create a group of everything except the result matrix
        everything_else = VGroup(matrix1, multiply_sign, matrix2, equals_sign)
        
        # Animate: fade out everything else and move/scale the result matrix to center
        self.play(
            FadeOut(everything_else),
            Transform(result_matrix, final_result_matrix),
            run_time=1
        )
        result_label = Text("Result Matrix", font_size=36).next_to(final_result_matrix, DOWN, buff=0.8)
        self.play(Write(result_label))
        
        # Final pause to display the result
        self.wait(3)
