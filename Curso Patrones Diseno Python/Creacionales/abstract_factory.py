"""Patrón Abstract Factory.

Problema
    Hay que crear FAMILIAS de objetos relacionados (botón + casilla del mismo
    estilo) y garantizar que nunca se mezclen productos de familias distintas.

Solución
    Una interfaz ``GUIFactory`` declara un método por cada producto de la
    familia. Cada fábrica concreta (``LightFactory``, ``DarkFactory``) crea
    todos los productos de SU familia. El cliente solo usa la interfaz
    abstracta, así que cambiar de familia es cambiar de fábrica.

Cuándo usar
    - El sistema debe funcionar con varias familias de productos
      (temas, sistemas operativos, motores de base de datos...).
    - Los productos de una familia están diseñados para usarse juntos.

Cuándo NO usar
    - Solo hay un producto o una familia: Factory Method o un constructor
      es suficiente.
    - Añadir un producto nuevo a la familia obliga a tocar todas las fábricas.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Button(ABC):
    theme: str

    @abstractmethod
    def render(self) -> str: ...


class Checkbox(ABC):
    theme: str

    @abstractmethod
    def render(self) -> str: ...


class LightButton(Button):
    theme = "light"

    def render(self) -> str:
        return "[ Botón claro ]"


class LightCheckbox(Checkbox):
    theme = "light"

    def render(self) -> str:
        return "[ ] Casilla clara"


class DarkButton(Button):
    theme = "dark"

    def render(self) -> str:
        return "[ Botón oscuro ]"


class DarkCheckbox(Checkbox):
    theme = "dark"

    def render(self) -> str:
        return "[x] Casilla oscura"


class GUIFactory(ABC):
    """Fábrica abstracta: un método de creación por producto de la familia."""

    @abstractmethod
    def create_button(self) -> Button: ...

    @abstractmethod
    def create_checkbox(self) -> Checkbox: ...


class LightFactory(GUIFactory):
    def create_button(self) -> Button:
        return LightButton()

    def create_checkbox(self) -> Checkbox:
        return LightCheckbox()


class DarkFactory(GUIFactory):
    def create_button(self) -> Button:
        return DarkButton()

    def create_checkbox(self) -> Checkbox:
        return DarkCheckbox()


def render_form(factory: GUIFactory) -> list[str]:
    """Código cliente: no sabe qué familia concreta está usando."""
    return [factory.create_button().render(), factory.create_checkbox().render()]


def demo() -> None:
    for factory in (LightFactory(), DarkFactory()):
        print(f"{type(factory).__name__}:")
        for linea in render_form(factory):
            print(f"  {linea}")


if __name__ == "__main__":
    demo()
