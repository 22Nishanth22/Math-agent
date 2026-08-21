import sympy
from typing import Literal
from langchain_core.tools import tool


@tool
def equations(string: str, mode: Literal['simplify', 'solve']):
    """Perform symbolic math computation on an expression or equation.

    Use this tool when the user asks to simplify a math expression,
    verify whether two expressions are equivalent, or solve an equation
    for its roots/solutions.

    Args:
        string: The math expression or equation as a plain text string,
            using standard Python math syntax (e.g., "x**2 - 4",
            "x**2 + 2*x + 1 - (x+1)**2").
        mode: Either "simplify" (reduce an expression to its simplest form,
            useful for checking if two expressions are equal) or "solve"
            (find the value(s) of the variable that satisfy the equation).

    Returns:
        The simplified expression, or the list of solutions.
    """
    expression = sympy.sympify(string)
    if mode == "simplify":
        return sympy.simplify(expression)
    elif mode == "solve":
        return sympy.solve(expression)
    else:
        print(f"Wrong Mode selected")