from typing import List
from agents import function_tool, FunctionTool

class MathTools:
    name = "MathTools"

    def __init__(self, description: str = "A tool for performing mathematical operations") -> None:
        self.description = description

    def __str__(self) -> str:
        return f"""Tool name: {self.name} \n description: {self.description}"""

    def get_tools(self, human_in_loop: bool = False) -> List[FunctionTool]:
        @function_tool
        def add(a: float, b: float) -> float:
            """
            Adds two numbers.

            Args:
                a (float): The first number.
                b (float): The second number.

            Returns:
                float: The sum of a and b.

            Example:
                >>> add(5, 3)
                8.0
            """
            return a + b

        @function_tool
        def substract(a: float, b: float) -> float:
            """
            Subtracts the second number from the first.

            Args:
                a (float): The number to subtract from.
                b (float): The number to subtract.

            Returns:
                float: The result of a minus b.

            Example:
                >>> subtract(10, 4)
                6.0
            """
            return a - b

        @function_tool
        def multiply(a: float, b: float) -> float:
            """
            Multiplies two numbers.

            Args:
                a (float): The first number.
                b (float): The second number.

            Returns:
                float: The product of a and b.

            Example:
                >>> multiply(4, 3)
                12.0
            """
            return a * b
        
        @function_tool
        def divide(a: float, b: float) -> float:
            """
            Divides the first number by the second.

            Args:
                a (float): The numerator.
                b (float): The denominator. Must not be zero.

            Returns:
                float: The result of a divided by b.

            Raises:
                ZeroDivisionError: If b is zero.

            Example:
                >>> divide(10, 2)
                5.0
            """
            return a / b
        
        @function_tool
        def square(a: float) -> float:
            """
            Returns the square of a number.

            Args:
                a (float): The number to square.

            Returns:
                float: The square of a.

            Example:
                >>> square(4)
                16.0
            """
            return a * a
        
        @function_tool
        def cube(a: float) -> float:
            """
            Returns the cube of a number.

            Args:
                a (float): The number to cube.

            Returns:
                float: The cube of a.

            Example:
                >>> cube(3)
                27.0
            """
            return a * a * a
        
        return [
            add,
            substract,
            multiply,
            divide,
            square,
            cube
        ]