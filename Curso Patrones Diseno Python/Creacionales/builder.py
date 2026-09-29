"""Patrón Builder.

Problema
    Un objeto con muchos parámetros (algunos obligatorios, otros opcionales)
    obliga a constructores telescópicos ilegibles y permite estados inválidos.

Solución
    Un ``Builder`` va acumulando la configuración paso a paso con una API
    fluida (cada método devuelve ``self``) y ``build()`` valida que estén los
    campos obligatorios antes de crear el producto final (inmutable).

Cuándo usar
    - Objetos complejos con muchas opciones y valores por defecto.
    - Se quiere construir en pasos y validar al final.
    - El mismo proceso puede producir representaciones distintas (Director).

Cuándo NO usar
    - Objetos con pocos campos: un ``dataclass`` o un constructor bastan.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Computer:
    """Producto final: inmutable una vez construido."""

    cpu: str
    ram_gb: int
    storage_gb: int = 256
    gpu: str | None = None

    def __str__(self) -> str:
        gpu = self.gpu or "integrada"
        return f"Computer(cpu={self.cpu}, ram={self.ram_gb}GB, disco={self.storage_gb}GB, gpu={gpu})"


class ComputerBuilder:
    """Constructor fluido. ``cpu`` y ``ram_gb`` son obligatorios."""

    def __init__(self) -> None:
        self._cpu: str | None = None
        self._ram_gb: int | None = None
        self._storage_gb: int = 256
        self._gpu: str | None = None

    def with_cpu(self, cpu: str) -> "ComputerBuilder":
        self._cpu = cpu
        return self

    def with_ram(self, gb: int) -> "ComputerBuilder":
        self._ram_gb = gb
        return self

    def with_storage(self, gb: int) -> "ComputerBuilder":
        self._storage_gb = gb
        return self

    def with_gpu(self, gpu: str) -> "ComputerBuilder":
        self._gpu = gpu
        return self

    def build(self) -> Computer:
        faltan = [
            nombre
            for nombre, valor in (("cpu", self._cpu), ("ram_gb", self._ram_gb))
            if valor is None
        ]
        if faltan:
            raise ValueError(f"Faltan campos obligatorios: {', '.join(faltan)}")
        assert self._cpu is not None and self._ram_gb is not None
        return Computer(self._cpu, self._ram_gb, self._storage_gb, self._gpu)


class Director:
    """Encapsula recetas de construcción reutilizables."""

    @staticmethod
    def gaming_pc(builder: ComputerBuilder) -> Computer:
        return builder.with_cpu("8 núcleos").with_ram(32).with_storage(1024).with_gpu("dedicada").build()

    @staticmethod
    def office_pc(builder: ComputerBuilder) -> Computer:
        return builder.with_cpu("4 núcleos").with_ram(8).build()


def demo() -> None:
    pc = ComputerBuilder().with_cpu("6 núcleos").with_ram(16).with_gpu("dedicada").build()
    print(f"API fluida    -> {pc}")
    print(f"Director gamer -> {Director.gaming_pc(ComputerBuilder())}")
    print(f"Director oficina -> {Director.office_pc(ComputerBuilder())}")
    try:
        ComputerBuilder().with_cpu("6 núcleos").build()
    except ValueError as error:
        print(f"Sin RAM       -> ValueError: {error}")


if __name__ == "__main__":
    demo()
