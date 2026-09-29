"""Patrón Composite (Estructural).

Problema:
    Hay que tratar igual a objetos individuales y a grupos de objetos
    (estructuras en árbol), sin que el cliente distinga uno de otro.

Solución:
    Una interfaz común para hojas y compuestos; el compuesto guarda hijos de
    esa misma interfaz y delega la operación en ellos recursivamente.

Cuándo usar:
    - Jerarquías parte-todo: carpetas/archivos, menús, pedidos con cajas.
    - Cuando el cliente debe ignorar la diferencia hoja/compuesto.

Cuándo NO usar:
    - Si los elementos no forman una jerarquía real.
    - Si hoja y compuesto necesitan interfaces muy distintas.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Component(ABC):
    """Interfaz común para hojas y compuestos."""

    @abstractmethod
    def total(self) -> float:
        """Precio total del componente (y de todo lo que contenga)."""

    @abstractmethod
    def render(self, indent: int = 0) -> str: ...


class Product(Component):
    """Hoja: no tiene hijos."""

    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def total(self) -> float:
        return self.price

    def render(self, indent: int = 0) -> str:
        return f"{'  ' * indent}- {self.name}: {self.price:.2f}"


class Box(Component):
    """Compuesto: contiene productos u otras cajas."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._children: list[Component] = []

    def add(self, child: Component) -> Box:
        self._children.append(child)
        return self

    def total(self) -> float:
        return sum(child.total() for child in self._children)

    def render(self, indent: int = 0) -> str:
        lines = [f"{'  ' * indent}+ {self.name} (total {self.total():.2f})"]
        lines += [c.render(indent + 1) for c in self._children]
        return "\n".join(lines)


def demo() -> None:
    inner = Box("Caja pequeña").add(Product("Cable", 5.0)).add(Product("Ratón", 15.0))
    outer = Box("Caja grande").add(Product("Teclado", 30.0)).add(inner)
    print(outer.render())
    print(f"Total del pedido: {outer.total():.2f}")


if __name__ == "__main__":
    demo()
