"""Memento (Recuerdo).

Problema
    Guardar y restaurar el estado de un objeto (deshacer) sin romper su
    encapsulación.

Solución
    El objeto (Originator) crea instantáneas inmutables (Memento) que solo él
    interpreta; el Cuidador (Caretaker) las apila sin mirarlas. Ejemplo: un
    editor de texto con deshacer.

Cuándo usar
    - Deshacer/rehacer, puntos de restauración, transacciones en memoria.

Cuándo NO usar
    - Estados muy grandes o frecuentes: consumo de memoria.
    - Basta invertir la operación: Command con ``undo``.

Solo stdlib, Python 3.11+.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Memento:
    """Instantánea inmutable del estado del editor."""

    _texto: str
    _cursor: int


class Editor:
    """Originator."""

    def __init__(self) -> None:
        self.texto = ""
        self.cursor = 0

    def escribir(self, s: str) -> None:
        self.texto = self.texto[: self.cursor] + s + self.texto[self.cursor :]
        self.cursor += len(s)

    def guardar(self) -> Memento:
        return Memento(self.texto, self.cursor)

    def restaurar(self, m: Memento) -> None:
        self.texto, self.cursor = m._texto, m._cursor


class Historial:
    """Caretaker: apila mementos sin conocer su contenido."""

    def __init__(self, editor: Editor) -> None:
        self._editor = editor
        self._pila: list[Memento] = []

    def snapshot(self) -> None:
        self._pila.append(self._editor.guardar())

    def deshacer(self) -> bool:
        if not self._pila:
            return False
        self._editor.restaurar(self._pila.pop())
        return True


def demo() -> None:
    ed = Editor()
    h = Historial(ed)
    for palabra in ("Hola", " mundo", "!!!"):
        h.snapshot()
        ed.escribir(palabra)
        print("Texto:", ed.texto)
    while h.deshacer():
        print("Deshacer ->", repr(ed.texto))


if __name__ == "__main__":
    demo()
