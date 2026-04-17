"""Simple command-line calculator in Python.

Supports basic arithmetic and power operations using a safe parser.
"""
import ast
import operator

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Mod: operator.mod,
}


def evaluate_expression(expression: str) -> float:
    """Evaluate a math expression safely using AST parsing."""
    try:
        node = ast.parse(expression, mode="eval")
        return _evaluate_node(node.body)
    except ZeroDivisionError:
        raise ValueError("Division by zero is not allowed.")
    except (SyntaxError, TypeError, ValueError):
        raise ValueError("Invalid expression. Use numbers and + - * / % ** only.")


def _evaluate_node(node):
    if isinstance(node, ast.BinOp):
        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported operator: {op_type.__name__}")
    if isinstance(node, ast.UnaryOp):
        operand = _evaluate_node(node.operand)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported operator: {op_type.__name__}")
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if hasattr(ast, "Num") and isinstance(node, ast.Num):
        return node.n
    raise ValueError("Unsupported expression element.")


def print_help() -> None:
    print("Python Calculator")
    print("Enter a math expression and press Enter.")
    print("Supported operations: +, -, *, /, %, **, parentheses")
    print("Example: 3 + 4 * (2 - 1) / 5")
    print("Type 'quit' or 'exit' to close the calculator.")
    print("made by bitetheapple")


def main() -> None:
    print_help()
    while True:
        try:
            expression = input("> ").strip()
            if expression.lower() in {"quit", "exit"}:
                print("Goodbye!")
                break
            if not expression:
                continue
            result = evaluate_expression(expression)
            print(result)
        except ValueError as exc:
            print(f"Error: {exc}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
