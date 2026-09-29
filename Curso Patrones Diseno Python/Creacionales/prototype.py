"""Patrón Prototype.

Problema
    Crear un objeto desde cero es caro o complicado (muchos campos, datos
    anidados, configuración previa) y queremos nuevos objetos parecidos a uno
    existente sin depender de su clase concreta.

Solución
    El propio objeto sabe copiarse: expone ``clone()``. La copia es PROFUNDA
    (``copy.deepcopy``), de modo que modificar el clon no afecta al original ni
    a sus objetos anidados (listas, diccionarios...).

Cuándo usar
    - Muchas variantes de un objeto que solo difieren en unos pocos campos.
    - Se quiere evitar una jerarquía de fábricas paralela a la de productos.
    - La inicialización es costosa y copiar es más barato.

Cuándo NO usar
    - Objetos simples: un constructor normal es más claro.
    - Objetos con recursos no copiables (sockets, ficheros abiertos, locks).
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Protocol, Self



class Prototype(Protocol):
    """Contrato: cualquier objeto que sepa devolver una copia de sí mismo."""

    def clone(self) -> Self: ...


@dataclass
class Shape:
    """Prototipo base: una figura con color y etiquetas mutables."""

    color: str
    tags: list[str] = field(default_factory=list)

    def clone(self) -> Self:
        # deepcopy copia también la lista `tags`; una copia superficial
        # compartiría la misma lista entre original y clon.
        return copy.deepcopy(self)


@dataclass
class Circle(Shape):
    radius: float = 1.0


@dataclass
class Rectangle(Shape):
    width: float = 1.0
    height: float = 1.0


class ShapeRegistry:
    """Catálogo de prototipos: se pide una copia por nombre."""

    def __init__(self) -> None:
        self._prototypes: dict[str, Shape] = {}

    def register(self, name: str, prototype: Shape) -> None:
        self._prototypes[name] = prototype

    def create(self, name: str) -> Shape:
        return self._prototypes[name].clone()


def demo() -> None:
    original = Circle(color="rojo", tags=["base"], radius=2.5)
    copia = original.clone()
    copia.color = "azul"
    copia.tags.append("copia")

    print(f"original -> {original}")
    print(f"clon     -> {copia}")
    print(f"comparten la lista tags? {original.tags is copia.tags}")

    registro = ShapeRegistry()
    registro.register("cuadrado", Rectangle(color="verde", width=2, height=2))
    print(f"desde el registro -> {registro.create('cuadrado')}")


if __name__ == "__main__":
    demo()
