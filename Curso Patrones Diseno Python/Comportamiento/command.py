"""Command (Comando).

Problema
    Quieres parametrizar acciones como objetos: encolarlas, registrarlas o
    deshacerlas, sin que quien las dispara conozca al receptor concreto.

Solución
    Encapsular cada petición en un objeto ``Command`` con ``execute()`` y
    ``undo()``. Un ``Invoker`` ejecuta comandos y guarda un historial (pila);
    deshacer saca el último comando y lo revierte (orden inverso).

Cuándo usar
    - Deshacer/rehacer, historial, macros, colas de tareas.
    - Desacoplar el emisor (botón, menú, CLI) del receptor que hace el trabajo.

Cuándo NO usar
    - La acción es trivial y no necesita deshacerse ni registrarse: una
      función normal basta.
    - Deshacer es imposible o carísimo (efectos externos irreversibles).

Ejemplo didáctico: un editor de texto con ``Write`` y ``Delete`` deshacibles.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class TextEditor:
    """Receptor: quien realmente hace el trabajo."""

    def __init__(self) -> None:
        self.text = ""


class Command(ABC):
    """Interfaz de comando."""

    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...


class WriteCommand(Command):
    """Añade texto al final del documento."""

    def __init__(self, editor: TextEditor, chunk: str) -> None:
        self.editor = editor
        self.chunk = chunk

    def execute(self) -> None:
        self.editor.text += self.chunk

    def undo(self) -> None:
        self.editor.text = self.editor.text[: len(self.editor.text) - len(self.chunk)]


class DeleteCommand(Command):
    """Borra los últimos ``count`` caracteres (recuerda lo borrado para deshacer)."""

    def __init__(self, editor: TextEditor, count: int) -> None:
        self.editor = editor
        self.count = count
        self._deleted = ""

    def execute(self) -> None:
        cut = max(len(self.editor.text) - self.count, 0)
        self._deleted = self.editor.text[cut:]
        self.editor.text = self.editor.text[:cut]

    def undo(self) -> None:
        self.editor.text += self._deleted


class Invoker:
    """Ejecuta comandos y mantiene la pila de historial para deshacer."""

    def __init__(self) -> None:
        self._history: list[Command] = []

    def run(self, command: Command) -> None:
        command.execute()
        self._history.append(command)

    def undo(self) -> bool:
        """Deshace el último comando. Devuelve False si no hay nada que deshacer."""
        if not self._history:
            return False
        self._history.pop().undo()
        return True

    @property
    def history_size(self) -> int:
        return len(self._history)


def demo() -> None:
    editor = TextEditor()
    invoker = Invoker()

    invoker.run(WriteCommand(editor, "Hola"))
    invoker.run(WriteCommand(editor, ", mundo"))
    invoker.run(DeleteCommand(editor, 3))
    print(f"Tras 3 comandos: {editor.text!r}")

    while invoker.undo():
        print(f"Deshacer -> {editor.text!r}")
    print("Historial vacío: nada más que deshacer.")


if __name__ == "__main__":
    demo()
