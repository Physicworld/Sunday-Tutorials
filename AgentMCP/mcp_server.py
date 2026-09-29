import ast
import operator
from datetime import datetime
from fastmcp import FastMCP

mcp = FastMCP("Demo Server for Ollama Agent")

MAX_EXPONENTE = 1000      # |exponente| máximo en '**'
MAX_MAGNITUD = 10 ** 100  # tope de valor absoluto en cualquier resultado intermedio
MAX_LONGITUD = 200        # caracteres máximos de la expresión
MAX_PROFUNDIDAD = 50      # profundidad máxima del árbol (evita RecursionError)

_BINARIOS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARIOS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _comprobar(valor):
    if abs(valor) > MAX_MAGNITUD:
        raise ValueError("resultado demasiado grande")
    return valor


def _evaluar(nodo, profundidad=0):
    if profundidad > MAX_PROFUNDIDAD:
        raise ValueError("expresión demasiado anidada")
    if isinstance(nodo, ast.Expression):
        return _evaluar(nodo.body, profundidad + 1)
    if isinstance(nodo, ast.Constant):
        # bool es subclase de int: se rechaza explícitamente
        if type(nodo.value) in (int, float):
            return _comprobar(nodo.value)
        raise ValueError("solo se permiten números")
    if isinstance(nodo, ast.UnaryOp) and type(nodo.op) in _UNARIOS:
        return _comprobar(_UNARIOS[type(nodo.op)](_evaluar(nodo.operand, profundidad + 1)))
    if isinstance(nodo, ast.BinOp) and type(nodo.op) in _BINARIOS:
        izq = _evaluar(nodo.left, profundidad + 1)
        der = _evaluar(nodo.right, profundidad + 1)
        if isinstance(nodo.op, ast.Pow) and abs(der) > MAX_EXPONENTE:
            raise ValueError(f"exponente demasiado grande (máximo {MAX_EXPONENTE})")
        return _comprobar(_BINARIOS[type(nodo.op)](izq, der))
    raise ValueError("operación no permitida")


def evaluar_expresion(expresion: str):
    """Evalúa aritmética básica sin eval(): números, + - * / // % ** y paréntesis.

    Lanza ValueError (expresión no permitida o demasiado costosa) o
    ZeroDivisionError.
    """
    if len(expresion) > MAX_LONGITUD:
        raise ValueError(f"expresión demasiado larga (máximo {MAX_LONGITUD} caracteres)")
    try:
        arbol = ast.parse(expresion.strip(), mode="eval")
    except (SyntaxError, RecursionError, MemoryError):
        raise ValueError("expresión no válida") from None
    try:
        return _evaluar(arbol)
    except OverflowError:
        raise ValueError("resultado demasiado grande") from None


@mcp.tool
def calcular(expresion: str) -> str:
    """Calcula una expresion matemática simple"""
    try:
        resultado = evaluar_expresion(expresion)
        return f"Resultado de '{expresion}' = {resultado}"
    except ValueError as e:
        return (f"Error: Solo se permiten números y operadores básicos "
                f"(+, -, *, /, //, %, **, ()): {e}")
    except Exception as e:
        return f"Error en cálculo: {str(e)}"


@mcp.tool
def fecha_actual() -> str:
    """Obtiene la fecha y hora actual"""
    now = datetime.now()
    return f"Fecha y hora actual: {now.strftime('%Y-%m-%d %H:%M:%S')}"


if __name__ == "__main__":
    print("🚀 Servidor MCP Demo iniciado")
    mcp.run()
