"""Método de bisección con evaluación segura de expresiones.

Uso:
    python Bisection.py --expr 'x**2-2' --a 0 --b 2 --tol 1e-6

Las expresiones se interpretan con ``ast`` en lista blanca (nunca ``eval``):
la variable ``x``, números, ``+ - * / **``, paréntesis y las funciones
``sin``, ``cos``, ``exp``, ``log`` y ``sqrt``.
"""
import argparse
import ast
import math
import operator
import sys

_BINARIOS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}
_UNARIOS = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_FUNCIONES = {
    "sin": math.sin,
    "cos": math.cos,
    "exp": math.exp,
    "log": math.log,
    "sqrt": math.sqrt,
}


def _compilar(nodo):
    """Convierte un nodo ast permitido en una función de x; rechaza el resto."""
    if isinstance(nodo, ast.Expression):
        return _compilar(nodo.body)
    if isinstance(nodo, ast.Constant) and type(nodo.value) in (int, float):
        valor = float(nodo.value)
        return lambda x: valor
    if isinstance(nodo, ast.Name) and nodo.id == "x":
        return lambda x: x
    if isinstance(nodo, ast.UnaryOp) and type(nodo.op) in _UNARIOS:
        op, operando = _UNARIOS[type(nodo.op)], _compilar(nodo.operand)
        return lambda x: op(operando(x))
    if isinstance(nodo, ast.BinOp) and type(nodo.op) in _BINARIOS:
        op, izq, der = _BINARIOS[type(nodo.op)], _compilar(nodo.left), _compilar(nodo.right)
        return lambda x: op(izq(x), der(x))
    if (isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name)
            and nodo.func.id in _FUNCIONES and len(nodo.args) == 1 and not nodo.keywords):
        fn, arg = _FUNCIONES[nodo.func.id], _compilar(nodo.args[0])
        return lambda x: fn(arg(x))
    raise ValueError(f"expresión no permitida: {ast.dump(nodo)[:60]}")


def parse_expression(expresion):
    """Devuelve f(x) para una expresión de texto, o lanza ValueError si no es válida."""
    try:
        arbol = ast.parse(expresion.strip(), mode="eval")
    except (SyntaxError, RecursionError):
        raise ValueError(f"expresión no válida: {expresion!r}") from None
    return _compilar(arbol)


def bisection(f, a, b, tol=1e-6, max_iter=100, verbose=False):
    """Raíz de f en [a, b] por bisección.

    Requiere f(a)·f(b) <= 0. Termina cuando |f(c)| < tol o el semiancho del
    intervalo es < tol. Lanza ValueError si no hay cambio de signo, si el
    intervalo o la tolerancia no son válidos, y RuntimeError si no converge
    en ``max_iter`` iteraciones.
    """
    if not a < b:
        raise ValueError(f"intervalo inválido: se requiere a < b (a={a}, b={b})")
    if tol <= 0 or max_iter < 1:
        raise ValueError("tol debe ser > 0 y max_iter >= 1")
    f_a, f_b = f(a), f(b)
    if f_a == 0:
        return a
    if f_b == 0:
        return b
    if f_a * f_b > 0:
        raise ValueError(
            f"f(a) y f(b) tienen el mismo signo (f({a})={f_a}, f({b})={f_b}): "
            "no hay garantía de raíz en el intervalo"
        )
    for i in range(1, max_iter + 1):
        c = (a + b) / 2
        f_c = f(c)
        if verbose:
            print(f"x_a: {a}  x_b: {b}  c: {c}  f_c: {f_c}  N_iters: {i}")
        if f_c == 0 or abs(f_c) < tol or (b - a) / 2 < tol:
            return c
        if f_a * f_c < 0:
            b = c
        else:
            a, f_a = c, f_c
    raise RuntimeError(f"no convergió en {max_iter} iteraciones")


def main(argv=None):
    p = argparse.ArgumentParser(description="Bisección segura (sin eval).")
    p.add_argument("--expr", help="expresión en x, p. ej. 'x**2-2'")
    p.add_argument("--a", type=float, help="cota inferior")
    p.add_argument("--b", type=float, help="cota superior")
    p.add_argument("--tol", type=float, default=None, help="tolerancia (defecto 1e-6)")
    p.add_argument("--max-iter", type=int, default=100, help="iteraciones máximas (defecto 100)")
    args = p.parse_args(argv)
    try:
        # Sin argumentos, modo interactivo como en el vídeo
        expr = args.expr if args.expr is not None else input("Ingrese la funcion a resolver: ")
        a = args.a if args.a is not None else float(input("Ingrese la cota inferior: "))
        b = args.b if args.b is not None else float(input("Ingrese la cota superior: "))
        tol = args.tol if args.tol is not None else (
            1e-6 if args.expr is not None else float(input("Ingrese la tolerancia: ")))
        raiz = bisection(parse_expression(expr), a, b, tol, args.max_iter, verbose=True)
    except (ValueError, RuntimeError, ArithmeticError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    print("La raiz buscada es: ", raiz)
    return 0


if __name__ == "__main__":
    sys.exit(main())
