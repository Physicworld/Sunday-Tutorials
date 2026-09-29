"""Patrón Decorator (Estructural).

Problema:
    Añadir responsabilidades a un objeto o función de forma dinámica sin
    crear una subclase por cada combinación de extras.

Solución:
    Envolver el objeto con otro que comparte su interfaz y añade
    comportamiento antes/después de delegar. Los envoltorios se apilan.
    Se muestran las dos formas: clases (objetos) y decoradores de función
    de Python (con `functools.wraps`).

Cuándo usar:
    - Combinaciones opcionales de comportamiento (extras, logging, caché).
    - Cuando la herencia produciría demasiadas subclases.

Cuándo NO usar:
    - Si el orden de los envoltorios confunde o hay que quitar uno del medio.
    - Si un simple parámetro o flag resuelve el problema.
"""

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import Any


# --- Decorator con objetos -------------------------------------------------
class Coffee:
    def cost(self) -> float:
        return 2.0

    def description(self) -> str:
        return "Café"


class CoffeeDecorator:
    """Base: misma interfaz que `Coffee`, delega en el objeto envuelto."""

    def __init__(self, inner: Coffee | CoffeeDecorator) -> None:
        self._inner = inner

    def cost(self) -> float:
        return self._inner.cost()

    def description(self) -> str:
        return self._inner.description()


class Milk(CoffeeDecorator):
    def cost(self) -> float:
        return self._inner.cost() + 0.5

    def description(self) -> str:
        return self._inner.description() + " + leche"


class Sugar(CoffeeDecorator):
    def cost(self) -> float:
        return self._inner.cost() + 0.2

    def description(self) -> str:
        return self._inner.description() + " + azúcar"


# --- Decorator de función --------------------------------------------------
def shout(func: Callable[..., str]) -> Callable[..., str]:
    """Convierte el resultado a mayúsculas."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> str:
        return func(*args, **kwargs).upper()

    return wrapper


def exclaim(func: Callable[..., str]) -> Callable[..., str]:
    """Añade '!' al resultado."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> str:
        return func(*args, **kwargs) + "!"

    return wrapper


@shout
@exclaim
def greet(name: str) -> str:
    """Saluda a `name`."""
    return f"hola {name}"


def demo() -> None:
    drink = Sugar(Milk(Coffee()))
    print(f"{drink.description()}: {drink.cost():.2f}")
    print(greet("mundo"))
    print(f"Nombre conservado por wraps: {greet.__name__}")


if __name__ == "__main__":
    demo()
