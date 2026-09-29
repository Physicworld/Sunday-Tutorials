"""Patrón Flyweight (Estructural).

Problema:
    Miles de objetos similares consumen demasiada memoria porque cada uno
    duplica datos idénticos.

Solución:
    Separar el estado intrínseco (compartido, inmutable) del extrínseco
    (propio de cada uso, se pasa por parámetro). Una fábrica reutiliza los
    flyweights ya creados.

Cuándo usar:
    - Muchísimos objetos con gran parte del estado repetido.
    - El estado extrínseco puede calcularse o pasarse desde fuera.

Cuándo NO usar:
    - Pocos objetos: la complejidad no compensa el ahorro.
    - Si casi todo el estado es único por objeto.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TreeType:
    """Flyweight: estado intrínseco (compartido e inmutable)."""

    name: str
    color: str
    texture: str

    def draw(self, x: int, y: int) -> str:
        # x, y son estado extrínseco: los aporta quien usa el flyweight
        return f"{self.name} ({self.color}) en ({x}, {y})"


class TreeTypeFactory:
    """Fábrica: devuelve siempre el mismo objeto para los mismos datos."""

    _types: dict[tuple[str, str, str], TreeType] = {}

    @classmethod
    def get(cls, name: str, color: str, texture: str) -> TreeType:
        key = (name, color, texture)
        if key not in cls._types:
            cls._types[key] = TreeType(name, color, texture)
        return cls._types[key]

    @classmethod
    def count(cls) -> int:
        return len(cls._types)

    @classmethod
    def clear(cls) -> None:
        cls._types.clear()


@dataclass
class Tree:
    """Contexto: guarda solo el estado extrínseco y una referencia compartida."""

    x: int
    y: int
    type: TreeType

    def draw(self) -> str:
        return self.type.draw(self.x, self.y)


def demo() -> None:
    TreeTypeFactory.clear()
    forest = [
        Tree(i, i * 2, TreeTypeFactory.get("Pino" if i % 2 else "Roble", "verde", "rugosa"))
        for i in range(6)
    ]
    for tree in forest[:3]:
        print(tree.draw())
    print(f"Árboles: {len(forest)}, tipos compartidos: {TreeTypeFactory.count()}")


if __name__ == "__main__":
    demo()
