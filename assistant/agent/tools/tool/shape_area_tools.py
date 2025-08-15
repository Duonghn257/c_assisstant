# tools/shape_area_tools.py

from agents import FunctionTool, function_tool
from typing import List

class ShapeAreaTools:
    name = "ShapeAreaTools"

    def __init__(self, description: str = "A tool for calculating the area of shapes") -> None:
        self.description = description

    def __str__(self) -> str:
        return f"""Tool name: {self.name} \n description: {self.description}"""

    def get_tools(self, human_in_loop: bool = False) -> List[FunctionTool]:
        @function_tool
        def calculate_square_area(side: float) -> float:
            """
            Calculates the area of a square.

            Args:
                side (float): The length of one side of the square. Must be positive.

            Returns:
                float: The area of the square.

            Raises:
                ValueError: If the side length is not positive.

            Example:
                >>> calculate_square_area(5)
                25.0
            """
            if side <= 0:
                raise ValueError("Side length must be positive.")
            return side * side

        @function_tool
        def calculate_rectangle_area(length: float, width: float) -> float:
            """
            Calculates the area of a rectangle.

            Args:
                length (float): The length of the rectangle. Must be positive.
                width (float): The width of the rectangle. Must be positive.

            Returns:
                float: The area of the rectangle.

            Raises:
                ValueError: If either length or width is not positive.

            Example:
                >>> calculate_rectangle_area(10, 4)
                40.0
            """
            if length <= 0 or width <= 0:
                raise ValueError("Length and width must be positive.")
            return length * width

        @function_tool
        def calculate_triangle_area(base: float, height: float) -> float:
            """
            Calculates the area of a triangle.

            Args:
                base (float): The base length of the triangle. Must be positive.
                height (float): The height of the triangle. Must be positive.

            Returns:
                float: The area of the triangle.

            Raises:
                ValueError: If either base or height is not positive.

            Example:
                >>> calculate_triangle_area(6, 3)
                9.0
            """
            if base <= 0 or height <= 0:
                raise ValueError("Base and height must be positive.")
            return 0.5 * base * height
        
        return [
            calculate_square_area,
            calculate_rectangle_area,
            calculate_triangle_area
        ]