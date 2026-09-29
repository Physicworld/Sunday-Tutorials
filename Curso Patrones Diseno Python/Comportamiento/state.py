"""State (Estado).

Problema
    El comportamiento de un objeto depende de su estado interno y acaba
    lleno de ``if/elif`` repetidos sobre ese estado.

Solución
    Representar cada estado como una clase con su propio comportamiento. El
    contexto delega en el estado actual, y cada estado decide a qué estado
    se transita. Las transiciones inválidas lanzan un error explícito.

Cuándo usar
    - Máquinas de estados: pedidos, semáforos, reproductores, conexiones.
    - Muchos condicionales que dependen de un "modo" del objeto.

Cuándo NO usar
    - Hay pocos estados y transiciones simples: un ``Enum`` y un ``if`` bastan.
    - Los estados no cambian el comportamiento, solo son datos.

Ejemplo didáctico: un pedido (Order) que va de Pending -> Paid -> Shipped ->
Delivered. Solo se puede cancelar antes de enviarlo.
"""

from __future__ import annotations


class InvalidTransition(Exception):
    """Se intentó una transición no permitida desde el estado actual."""


class OrderState:
    """Estado base: por defecto ninguna transición es válida."""

    name = "Base"

    def pay(self, order: Order) -> None:
        raise InvalidTransition(f"No se puede pagar un pedido en estado {self.name}")

    def ship(self, order: Order) -> None:
        raise InvalidTransition(f"No se puede enviar un pedido en estado {self.name}")

    def deliver(self, order: Order) -> None:
        raise InvalidTransition(f"No se puede entregar un pedido en estado {self.name}")

    def cancel(self, order: Order) -> None:
        raise InvalidTransition(f"No se puede cancelar un pedido en estado {self.name}")


class Pending(OrderState):
    name = "Pending"

    def pay(self, order: Order) -> None:
        order.state = Paid()

    def cancel(self, order: Order) -> None:
        order.state = Cancelled()


class Paid(OrderState):
    name = "Paid"

    def ship(self, order: Order) -> None:
        order.state = Shipped()

    def cancel(self, order: Order) -> None:
        order.state = Cancelled()


class Shipped(OrderState):
    name = "Shipped"

    def deliver(self, order: Order) -> None:
        order.state = Delivered()


class Delivered(OrderState):
    name = "Delivered"  # estado final


class Cancelled(OrderState):
    name = "Cancelled"  # estado final


class Order:
    """Contexto: delega cada operación en su estado actual."""

    def __init__(self) -> None:
        self.state: OrderState = Pending()

    @property
    def status(self) -> str:
        return self.state.name

    def pay(self) -> None:
        self.state.pay(self)

    def ship(self) -> None:
        self.state.ship(self)

    def deliver(self) -> None:
        self.state.deliver(self)

    def cancel(self) -> None:
        self.state.cancel(self)


def demo() -> None:
    order = Order()
    print(f"Estado inicial: {order.status}")
    for action in (order.pay, order.ship, order.deliver):
        action()
        print(f"Tras {action.__name__}(): {order.status}")

    # Transición inválida: un pedido entregado no se puede cancelar
    try:
        order.cancel()
    except InvalidTransition as error:
        print(f"Error esperado: {error}")


if __name__ == "__main__":
    demo()
