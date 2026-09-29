"""Proxy (Sustituto).

Problema
    Acceder a un objeto costoso (p. ej. cargar un informe pesado) o
    restringido, sin que el cliente gestione ese coste ni los permisos.

Solución
    Un sustituto con la MISMA interfaz que el objeto real que controla el
    acceso. Aquí hay dos: un proxy virtual (carga perezosa + caché) y un proxy
    de protección (solo deja pasar al rol ``admin``).

Cuándo usar
    - Carga perezosa, caché, control de acceso, registro de llamadas.

Cuándo NO usar
    - No hay coste ni control que justifique el intermediario.
    - Solo quieres añadir comportamiento: usa Decorator.

Solo stdlib, Python 3.11+.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Informe(ABC):
    """Interfaz común (Subject)."""

    @abstractmethod
    def leer(self) -> str: ...


class InformeReal(Informe):
    """Objeto costoso (RealSubject): simula una carga lenta."""

    cargas = 0  # contador de "descargas" para poder observarlo en los tests

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        InformeReal.cargas += 1
        self._contenido = f"Contenido confidencial de {nombre}"

    def leer(self) -> str:
        return self._contenido


class InformeVirtualProxy(Informe):
    """Proxy virtual: crea el informe real solo cuando hace falta."""

    def __init__(self, nombre: str) -> None:
        self._nombre = nombre
        self._real: InformeReal | None = None

    def leer(self) -> str:
        if self._real is None:
            self._real = InformeReal(self._nombre)
        return self._real.leer()


class InformeProteccionProxy(Informe):
    """Proxy de protección: comprueba el rol antes de delegar."""

    def __init__(self, destino: Informe, rol: str) -> None:
        self._destino = destino
        self._rol = rol

    def leer(self) -> str:
        if self._rol != "admin":
            raise PermissionError(f"El rol '{self._rol}' no puede leer el informe")
        return self._destino.leer()


def demo() -> None:
    InformeReal.cargas = 0
    informe = InformeVirtualProxy("Q3")
    print("Proxy creado; cargas reales:", InformeReal.cargas)
    print(InformeProteccionProxy(informe, "admin").leer())
    print(informe.leer())
    print("Cargas reales tras dos lecturas:", InformeReal.cargas)
    try:
        InformeProteccionProxy(informe, "invitado").leer()
    except PermissionError as e:
        print("Denegado:", e)


if __name__ == "__main__":
    demo()
