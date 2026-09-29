"""Patrón Factory Method.

Problema
    Una clase necesita crear objetos pero no debe conocer la clase concreta
    del producto; si hace ``Truck()`` o ``Ship()`` directamente queda acoplada
    y añadir un tipo nuevo obliga a modificarla.

Solución
    La clase base (``Logistics``) declara un método fábrica ``create_transport``
    y contiene la lógica común (``plan_delivery``). Cada subclase creadora
    sobrescribe el método fábrica y devuelve su propio tipo de producto.

Cuándo usar
    - No se sabe de antemano el tipo exacto de objetos a crear.
    - Se quiere que las subclases decidan qué crear (extensión sin modificar).

Cuándo NO usar
    - Solo hay un producto y no se espera que cambie: un constructor basta.
    - Si el tipo se elige por un dato en tiempo de ejecución sin necesidad de
      subclases, un simple diccionario ``nombre -> clase`` es más sencillo.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Transport(ABC):
    """Producto: interfaz común de todos los transportes."""

    @abstractmethod
    def deliver(self, cargo: str) -> str: ...


class Truck(Transport):
    def deliver(self, cargo: str) -> str:
        return f"Camión entrega '{cargo}' por carretera"


class Ship(Transport):
    def deliver(self, cargo: str) -> str:
        return f"Barco entrega '{cargo}' por mar"


class Logistics(ABC):
    """Creador: contiene lógica de negocio que usa el producto sin conocer su clase."""

    @abstractmethod
    def create_transport(self) -> Transport:
        """Método fábrica: las subclases deciden qué producto crear."""

    def plan_delivery(self, cargo: str) -> str:
        transport = self.create_transport()
        return transport.deliver(cargo)


class RoadLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Truck()


class SeaLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Ship()


def demo() -> None:
    for creador in (RoadLogistics(), SeaLogistics()):
        producto = creador.create_transport()
        print(f"{type(creador).__name__:15} crea {type(producto).__name__:6} -> {creador.plan_delivery('paquetes')}")


if __name__ == "__main__":
    demo()
