import sympy as sp

from interfaces.profiling import profiling
from interfaces.gemini import ask_gemini
from resources.dialogue_library import error_responses_math

@profiling
def solve_expression(expression):
    try:
        result = sp.sympify(expression).evalf()
        success_response = ask_gemini(f"Rephrase this as an ai assistant named zen: After some calculations, I've determined the answer is {result}.")

        return success_response

    except (sp.SympifyError, TypeError, SyntaxError):  
        return error_responses_math()

    except Exception as e:
      return f"An unexpected error occurred: {e}"


def expression_interpretation(expression):
    expression = (
        expression.replace("plus", "+")
        .replace("minus", "-")
        .replace("times", "*")
        .replace("multiplied by", "*")
        .replace("into", "*")
        .replace("divided by", "/")
        .replace("over", "/")
        .replace("to the power of", "**")
    )
    return expression