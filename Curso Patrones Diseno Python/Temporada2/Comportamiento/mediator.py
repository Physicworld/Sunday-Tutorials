"""Mediator (Mediador).

Problema
    Varios objetos se hablan entre sí directamente y forman una maraña de
    dependencias: añadir uno obliga a tocar a todos.

Solución
    Un mediador centraliza la comunicación; los colegas solo conocen al
    mediador. Ejemplo: una sala de chat donde los usuarios no se referencian
    entre sí.

Cuándo usar
    - Muchas interacciones muchos-a-muchos entre objetos acoplados.

Cuándo NO usar
    - Pocos objetos: el mediador se vuelve un "objeto dios".
    - Comunicación uno-a-muchos sin coordinación: Observer.

Solo stdlib, Python 3.11+.
"""
from __future__ import annotations


class SalaChat:
    """Mediator: registra usuarios y reparte los mensajes."""

    def __init__(self) -> None:
        self._usuarios: dict[str, Usuario] = {}

    def unirse(self, usuario: Usuario) -> None:
        if usuario.nombre in self._usuarios:
            raise ValueError(f"El nombre '{usuario.nombre}' ya está en uso")
        self._usuarios[usuario.nombre] = usuario
        usuario.sala = self

    def enviar(self, origen: Usuario, texto: str, destino: str | None = None) -> None:
        """Difunde a todos (menos al emisor) o entrega en privado."""
        if destino is not None:
            if destino not in self._usuarios:
                raise KeyError(f"Usuario desconocido: {destino}")
            self._usuarios[destino].recibir(origen.nombre, texto)
            return
        for nombre, u in self._usuarios.items():
            if nombre != origen.nombre:
                u.recibir(origen.nombre, texto)


class Usuario:
    """Colega: solo conoce a la sala, nunca a otros usuarios."""

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.sala: SalaChat | None = None
        self.bandeja: list[str] = []

    def enviar(self, texto: str, destino: str | None = None) -> None:
        if self.sala is None:
            raise RuntimeError("El usuario no está en ninguna sala")
        self.sala.enviar(self, texto, destino)

    def recibir(self, origen: str, texto: str) -> None:
        self.bandeja.append(f"{origen}: {texto}")


def demo() -> None:
    sala = SalaChat()
    ana, luis, eva = Usuario("ana"), Usuario("luis"), Usuario("eva")
    for u in (ana, luis, eva):
        sala.unirse(u)
    ana.enviar("Hola a todos")
    luis.enviar("Solo para ti, Ana", destino="ana")
    for u in (ana, luis, eva):
        print(u.nombre, "->", u.bandeja)


if __name__ == "__main__":
    demo()
