"""Patrón Template Method (Comportamiento) — Temporada 2.

Problema: varios algoritmos comparten los mismos pasos y el mismo orden, y
solo cambian los detalles de algunos pasos.

Solución: la clase base define el esqueleto (`preparar`, método plantilla)
y las subclases rellenan los pasos variables. Ejemplo: preparar bebidas.

Solo stdlib, Python 3.11+.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Bebida(ABC):
    def preparar(self) -> list[str]:
        """Método plantilla: el orden es fijo y las subclases no lo cambian."""
        pasos = ["hervir agua"]
        pasos.append(self.infusionar())
        pasos.append("servir en taza")
        if self.quiere_extras():  # hook opcional
            pasos.append(self.extras())
        return pasos

    @abstractmethod
    def infusionar(self) -> str: ...

    @abstractmethod
    def extras(self) -> str: ...

    def quiere_extras(self) -> bool:
        """Hook con comportamiento por defecto."""
        return True


class Te(Bebida):
    def infusionar(self) -> str:
        return "infusionar el té 3 minutos"

    def extras(self) -> str:
        return "añadir limón"


class Cafe(Bebida):
    def __init__(self, con_azucar: bool = True) -> None:
        self._con_azucar = con_azucar

    def infusionar(self) -> str:
        return "filtrar el café"

    def extras(self) -> str:
        return "añadir azúcar"

    def quiere_extras(self) -> bool:
        return self._con_azucar


def demo() -> None:
    for bebida in (Te(), Cafe(), Cafe(con_azucar=False)):
        print(type(bebida).__name__, "->", " / ".join(bebida.preparar()))


if __name__ == "__main__":
    demo()
