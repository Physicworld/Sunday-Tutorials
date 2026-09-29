"""Patrón Facade (Estructural).

Problema:
    Un conjunto de subsistemas con muchas clases y un orden de uso delicado
    obliga al cliente a conocer todos los detalles.

Solución:
    Ofrecer una clase fachada con una interfaz simple que orquesta los
    subsistemas en el orden correcto. Los subsistemas siguen accesibles.

Cuándo usar:
    - Simplificar el uso de una librería o subsistema complejo.
    - Definir un punto de entrada por capas.

Cuándo NO usar:
    - Si el subsistema ya es simple.
    - Si la fachada acaba siendo una "clase dios" que hace de todo.
"""

from __future__ import annotations


class Amplifier:
    def __init__(self, log: list[str]) -> None:
        self._log = log

    def on(self) -> None:
        self._log.append("Amplifier: encendido")


class Projector:
    def __init__(self, log: list[str]) -> None:
        self._log = log

    def on(self) -> None:
        self._log.append("Projector: encendido")

    def set_input(self, source: str) -> None:
        self._log.append(f"Projector: entrada {source}")


class Player:
    def __init__(self, log: list[str]) -> None:
        self._log = log

    def play(self, movie: str) -> None:
        self._log.append(f"Player: reproduciendo {movie}")


class HomeTheaterFacade:
    """Fachada: `watch_movie` orquesta los tres subsistemas en orden."""

    def __init__(self) -> None:
        self.log: list[str] = []
        self._amp = Amplifier(self.log)
        self._projector = Projector(self.log)
        self._player = Player(self.log)

    def watch_movie(self, movie: str) -> list[str]:
        self._amp.on()
        self._projector.on()
        self._projector.set_input("HDMI")
        self._player.play(movie)
        return self.log


def demo() -> None:
    theater = HomeTheaterFacade()
    for line in theater.watch_movie("El Padrino"):
        print(line)


if __name__ == "__main__":
    demo()
