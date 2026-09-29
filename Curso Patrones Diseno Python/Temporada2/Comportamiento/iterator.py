"""Iterator (Iterador).

Problema
    Recorrer una colección sin exponer su estructura interna y poder ofrecer
    varias formas de recorrerla.

Solución
    Separar el recorrido de la colección. En Python el patrón vive en el
    protocolo ``__iter__``/``__next__`` y en los generadores. Ejemplo: una
    playlist con recorrido normal, inverso y aleatorio con semilla.

Cuándo usar
    - Ocultar la estructura interna y permitir varios recorridos.

Cuándo NO usar
    - Una lista y un ``for`` ya bastan (en Python el patrón ya viene incluido).

Solo stdlib, Python 3.11+.
"""
from __future__ import annotations

import random
from collections.abc import Iterator


class Playlist:
    """Colección (Aggregate): guarda las canciones en una lista privada."""

    def __init__(self, canciones: list[str]) -> None:
        self._canciones = list(canciones)

    def __iter__(self) -> Iterator[str]:
        return IteradorPlaylist(self._canciones)

    def inverso(self) -> Iterator[str]:
        """Otro recorrido, escrito como generador."""
        for i in range(len(self._canciones) - 1, -1, -1):
            yield self._canciones[i]

    def aleatorio(self, semilla: int) -> Iterator[str]:
        copia = list(self._canciones)
        random.Random(semilla).shuffle(copia)
        yield from copia


class IteradorPlaylist:
    """Iterador explícito (Iterator): mantiene su propia posición."""

    def __init__(self, canciones: list[str]) -> None:
        self._canciones = canciones
        self._pos = 0

    def __iter__(self) -> IteradorPlaylist:
        return self

    def __next__(self) -> str:
        if self._pos >= len(self._canciones):
            raise StopIteration
        cancion = self._canciones[self._pos]
        self._pos += 1
        return cancion


def demo() -> None:
    p = Playlist(["A", "B", "C"])
    print("Normal:  ", list(p))
    print("Inverso: ", list(p.inverso()))
    print("Aleatorio:", list(p.aleatorio(semilla=1)))


if __name__ == "__main__":
    demo()
