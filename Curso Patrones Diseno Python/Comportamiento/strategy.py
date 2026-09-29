"""Strategy (Estrategia).

Problema
    Existen varias formas de hacer una misma tarea (un algoritmo) y elegir
    entre ellas con ``if/else`` dentro de la clase la vuelve rígida.

Solución
    Extraer cada algoritmo a una clase con la misma interfaz (``Strategy``).
    El contexto recibe una estrategia y la usa sin conocer su implementación;
    se puede intercambiar en tiempo de ejecución sin modificar el contexto.

Cuándo usar
    - Varias variantes de un algoritmo (ordenación, precios, compresión).
    - Quieres cambiar el comportamiento en ejecución o probar cada variante
      por separado.

Cuándo NO usar
    - Solo hay un algoritmo o las variantes casi nunca cambian.
    - Un simple parámetro o una función pasada como argumento es suficiente.

Ejemplo didáctico: carrito de compra con distintas estrategias de descuento.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Interfaz común de todas las estrategias de descuento."""

    @abstractmethod
    def apply(self, total: float) -> float:
        """Devuelve el total a pagar tras aplicar el descuento."""


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float) -> None:
        self.percent = percent

    def apply(self, total: float) -> float:
        return total * (1 - self.percent / 100)


class FixedDiscount(DiscountStrategy):
    def __init__(self, amount: float) -> None:
        self.amount = amount

    def apply(self, total: float) -> float:
        return max(total - self.amount, 0.0)  # nunca negativo


class ShoppingCart:
    """Contexto: usa la estrategia sin saber cuál es."""

    def __init__(self, strategy: DiscountStrategy | None = None) -> None:
        self.strategy: DiscountStrategy = strategy or NoDiscount()
        self._prices: list[float] = []

    def add(self, price: float) -> None:
        self._prices.append(price)

    def set_strategy(self, strategy: DiscountStrategy) -> None:
        """Intercambia la estrategia en tiempo de ejecución."""
        self.strategy = strategy

    def total(self) -> float:
        return self.strategy.apply(sum(self._prices))


def demo() -> None:
    cart = ShoppingCart()
    cart.add(60.0)
    cart.add(40.0)

    print(f"Sin descuento: {cart.total():.2f}")
    cart.set_strategy(PercentageDiscount(10))
    print(f"10% de descuento: {cart.total():.2f}")
    cart.set_strategy(FixedDiscount(25))
    print(f"25 fijos de descuento: {cart.total():.2f}")


if __name__ == "__main__":
    demo()
