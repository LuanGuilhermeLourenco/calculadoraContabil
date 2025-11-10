import ast
import operator
import math

# Dicionário de operadores suportados
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}

# Funções matemáticas permitidas
ALLOWED_FUNCS = {
    name: obj for name, obj in math.__dict__.items() if not name.startswith("__")
}
ALLOWED_FUNCS["abs"] = abs
ALLOWED_FUNCS["round"] = round


class SafeEvaluator:
    """Interpretador seguro baseado em AST."""

    def eval(self, expression: str):
        try:
            tree = ast.parse(expression, mode='eval')
            return self._eval_node(tree.body)
        except Exception as e:
            return f"Erro: expressão inválida ({e})"

    def _eval_node(self, node):
        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)
            if op_type in OPERATORS:
                return OPERATORS[op_type](left, right)
            raise TypeError(f"Operador não suportado: {op_type}")

        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op_type = type(node.op)
            if op_type in OPERATORS:
                return OPERATORS[op_type](operand)
            raise TypeError(f"Operador unário não suportado: {op_type}")

        elif isinstance(node, ast.Num):  # Python 3.8-
            return node.n
        elif isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.Call):
            func_name = node.func.id
            if func_name in ALLOWED_FUNCS:
                args = [self._eval_node(a) for a in node.args]
                return ALLOWED_FUNCS[func_name](*args)
            raise NameError(f"Função '{func_name}' não permitida.")
        else:
            raise TypeError(f"Nó AST não suportado: {type(node)}")


class Calculator:
    """Calculadora com histórico."""
    def __init__(self):
        self.history = []
        self.engine = SafeEvaluator()

    def evaluate(self, expression):
        result = self.engine.eval(expression)
        self.history.append((expression, result))
        return result

    def show_history(self):
        if not self.history:
            print("Histórico vazio.")
        for expr, res in self.history:
            print(f"{expr} = {res}")


def main():
    print("=== CALCULADORA AVANÇADA DE OPERACOES CONTABIES ===")
    print("Suporta funções avançadas de calculos matematicos.")
    print("Caso precise verificar o calculo pode colocar (Historico) ou entao (Sair) para encerrar")

    calc = Calculator()

    while True:
        expr = input("Digite seu Calculo:").strip()
        if expr.lower() == "sair":
            break
        elif expr.lower() == "historico":
            calc.show_history()
        elif expr == "":
            continue
        else:
            print(calc.evaluate(expr))


if __name__ == "__main__":
    main()