"""Chain of Responsibility (Cadena de Responsabilidad).

Problema
    Una petición puede ser atendida por distintos objetos y el emisor no
    debería saber cuál de ellos la resuelve (ni acoplarse a todos).

Solución
    Encadenar los manejadores (handlers). Cada uno decide si atiende la
    petición o la pasa al siguiente eslabón. El orden de la cadena determina
    la prioridad.

Cuándo usar
    - Varios objetos pueden atender la petición y el manejador correcto se
      decide en tiempo de ejecución (soporte por niveles, aprobaciones,
      filtros/middleware).
    - Quieres poder reordenar, añadir o quitar manejadores sin tocar al cliente.

Cuándo NO usar
    - Solo hay un manejador posible: una llamada directa es más simple.
    - Es obligatorio que la petición sea atendida y no puedes tolerar que
      "caiga" al final de la cadena sin respuesta.

Ejemplo didáctico: aprobación de gastos. Un gerente aprueba hasta 1.000, un
director hasta 10.000 y un CEO hasta 100.000. Por encima nadie lo aprueba.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Handler(ABC):
    """Eslabón abstracto de la cadena."""

    def __init__(self) -> None:
        self._next: Handler | None = None

    def set_next(self, handler: Handler) -> Handler:
        """Enlaza el siguiente manejador y lo devuelve (permite encadenar)."""
        self._next = handler
        return handler

    def handle(self, amount: float) -> str | None:
        """Atiende la petición o la delega. Devuelve None si nadie la maneja."""
        if self.can_handle(amount):
            return self.approve(amount)
        if self._next is not None:
            return self._next.handle(amount)
        return None  # fin de la cadena: petición no manejada

    @abstractmethod
    def can_handle(self, amount: float) -> bool:
        """Indica si este eslabón puede resolver la petición."""

    @abstractmethod
    def approve(self, amount: float) -> str:
        """Resuelve la petición y devuelve una descripción del resultado."""


class LimitHandler(Handler):
    """Manejador que aprueba importes hasta un límite."""

    def __init__(self, role: str, limit: float) -> None:
        super().__init__()
        self.role = role
        self.limit = limit

    def can_handle(self, amount: float) -> bool:
        return amount <= self.limit

    def approve(self, amount: float) -> str:
        return f"{self.role} aprobó {amount:,.0f}"


class Manager(LimitHandler):
    def __init__(self) -> None:
        super().__init__("Manager", 1_000)


class Director(LimitHandler):
    def __init__(self) -> None:
        super().__init__("Director", 10_000)


class CEO(LimitHandler):
    def __init__(self) -> None:
        super().__init__("CEO", 100_000)


def build_chain() -> Handler:
    """Construye la cadena Manager -> Director -> CEO y devuelve el primero."""
    manager = Manager()
    manager.set_next(Director()).set_next(CEO())
    return manager


def demo() -> None:
    chain = build_chain()
    for amount in (500, 5_000, 50_000, 500_000):
        result = chain.handle(amount)
        print(f"Gasto {amount:>7,}: {result or 'nadie pudo aprobarlo (petición no manejada)'}")


if __name__ == "__main__":
    demo()
