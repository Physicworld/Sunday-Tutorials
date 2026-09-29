"""Visitor (Visitante).

Problema
    Quieres añadir operaciones nuevas a una jerarquía de clases estable
    (calcular área, exportar...) sin modificar cada clase ni llenarlas de
    métodos ajenos a su responsabilidad.

Solución
    Cada elemento expone ``aceptar(visitante)`` y llama al método del
    visitante que corresponde a su tipo (doble despacho). Las operaciones
    nuevas son visitantes nuevos. Ejemplo: figuras geométricas con visitantes
    de área y de exportación a texto.

Cuándo usar
    - Jerarquía estable con operaciones que cambian o crecen a menudo.

Cuándo NO usar
    - Se añaden clases nuevas con frecuencia: cada una obliga a tocar todos
      los visitantes.
    - Con ``match`` o ``functools.singledispatch`` en Python suele bastar.

Solo stdlib, Python 3.11+.
"""
from __future__ import annotations

import math
from abc import ABC, abstractmethod


class Figura(ABC):
    @abstractmethod
    def aceptar(self, visitante: VisitanteFigura):
        ...


class Circulo(Figura):
    def __init__(self, radio: float) -> None:
        self.radio = radio

    def aceptar(self, visitante: VisitanteFigura):
        return visitante.visitar_circulo(self)


class Rectangulo(Figura):
    def __init__(self, ancho: float, alto: float) -> None:
        self.ancho = ancho
        self.alto = alto

    def aceptar(self, visitante: VisitanteFigura):
        return visitante.visitar_rectangulo(self)


class VisitanteFigura(ABC):
    @abstractmethod
    def visitar_circulo(self, c: Circulo): ...

    @abstractmethod
    def visitar_rectangulo(self, r: Rectangulo): ...


class CalculadorArea(VisitanteFigura):
    def visitar_circulo(self, c: Circulo) -> float:
        return math.pi * c.radio**2

    def visitar_rectangulo(self, r: Rectangulo) -> float:
        return r.ancho * r.alto


class ExportadorTexto(VisitanteFigura):
    def visitar_circulo(self, c: Circulo) -> str:
        return f"Circulo(radio={c.radio})"

    def visitar_rectangulo(self, r: Rectangulo) -> str:
        return f"Rectangulo({r.ancho}x{r.alto})"


def demo() -> None:
    figuras = [Circulo(1), Rectangulo(2, 3)]
    for v in (CalculadorArea(), ExportadorTexto()):
        print(type(v).__name__, [f.aceptar(v) for f in figuras])


if __name__ == "__main__":
    demo()
