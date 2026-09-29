"""Interpreter (Intérprete).

Problema
    Tienes un lenguaje pequeño y repetitivo (reglas, fórmulas, filtros) y
    quieres evaluar expresiones en ese lenguaje.

Solución
    Representar la gramática como clases: cada regla es una expresión con
    ``interpretar(contexto)``. Un parser mínimo construye el árbol. Ejemplo:
    aritmética con variables, ``+ - * /``, paréntesis y ``x``, ``y``...

Cuándo usar
    - Lenguajes pequeños y estables (reglas de negocio, filtros).

Cuándo NO usar
    - Gramáticas grandes o complejas: usa un generador de parsers.
    - Basta ``ast.literal_eval`` o una función normal.
    - NUNCA uses ``eval`` con entradas de usuarios: aquí el parser solo
      acepta la gramática definida.

Solo stdlib, Python 3.11+.
"""
from __future__ import annotations

import re
from abc import ABC, abstractmethod
from operator import add, mul, sub, truediv


class Expresion(ABC):
    @abstractmethod
    def interpretar(self, contexto: dict[str, float]) -> float: ...


class Numero(Expresion):
    def __init__(self, valor: float) -> None:
        self.valor = valor

    def interpretar(self, contexto: dict[str, float]) -> float:
        return self.valor


class Variable(Expresion):
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre

    def interpretar(self, contexto: dict[str, float]) -> float:
        if self.nombre not in contexto:
            raise NameError(f"Variable no definida: {self.nombre}")
        return contexto[self.nombre]


class Binaria(Expresion):
    _OPS = {"+": add, "-": sub, "*": mul, "/": truediv}

    def __init__(self, op: str, izq: Expresion, der: Expresion) -> None:
        self.op, self.izq, self.der = op, izq, der

    def interpretar(self, contexto: dict[str, float]) -> float:
        return self._OPS[self.op](
            self.izq.interpretar(contexto), self.der.interpretar(contexto)
        )


_TOKEN = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|([A-Za-z_]\w*)|(.))")


def _tokenizar(texto: str) -> list[str]:
    tokens = []
    for num, nombre, otro in _TOKEN.findall(texto):
        tokens.append(num or nombre or otro)
    return [t for t in tokens if t.strip()]


class Parser:
    """Descenso recursivo. Gramática:

        expr   := term (('+'|'-') term)*
        term   := factor (('*'|'/') factor)*
        factor := NUMERO | NOMBRE | '(' expr ')'
    """

    def __init__(self, texto: str) -> None:
        self._t = _tokenizar(texto)
        self._i = 0

    def parsear(self) -> Expresion:
        nodo = self._expr()
        if self._i != len(self._t):
            raise SyntaxError(f"Token inesperado: {self._t[self._i]}")
        return nodo

    def _peek(self) -> str | None:
        return self._t[self._i] if self._i < len(self._t) else None

    def _next(self) -> str:
        if self._i >= len(self._t):
            raise SyntaxError("Expresión incompleta")
        tok = self._t[self._i]
        self._i += 1
        return tok

    def _expr(self) -> Expresion:
        nodo = self._term()
        while self._peek() in ("+", "-"):
            nodo = Binaria(self._next(), nodo, self._term())
        return nodo

    def _term(self) -> Expresion:
        nodo = self._factor()
        while self._peek() in ("*", "/"):
            nodo = Binaria(self._next(), nodo, self._factor())
        return nodo

    def _factor(self) -> Expresion:
        tok = self._next()
        if tok == "(":
            nodo = self._expr()
            if self._next() != ")":
                raise SyntaxError("Falta ')'")
            return nodo
        if re.fullmatch(r"\d+(\.\d+)?", tok):
            return Numero(float(tok))
        if re.fullmatch(r"[A-Za-z_]\w*", tok):
            return Variable(tok)
        raise SyntaxError(f"Token inesperado: {tok}")


def evaluar(texto: str, **variables: float) -> float:
    return Parser(texto).parsear().interpretar(variables)


def demo() -> None:
    print("2 + 3 * 4       =", evaluar("2 + 3 * 4"))
    print("(2 + 3) * 4     =", evaluar("(2 + 3) * 4"))
    print("x * (y - 1), x=5, y=3 =", evaluar("x * (y - 1)", x=5, y=3))


if __name__ == "__main__":
    demo()
