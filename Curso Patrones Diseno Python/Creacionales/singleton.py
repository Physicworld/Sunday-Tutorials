"""Patrón Singleton.

Problema
    Necesitamos que una clase tenga UNA sola instancia en todo el programa
    (configuración global, pool de conexiones, registro de logs) y que todo el
    código acceda a esa misma instancia.

Solución
    La clase controla su propia creación: ``__new__`` devuelve siempre el mismo
    objeto. Aquí se protege la creación con un ``Lock`` (doble comprobación)
    para que sea seguro con hilos.

Cuándo usar
    - Debe existir exactamente una instancia de un recurso compartido.
    - Se quiere un punto de acceso global controlado.

Cuándo NO usar
    - Solo por comodidad para tener "variables globales": oculta dependencias y
      dificulta los tests (el estado persiste entre pruebas).
    - Si basta con un módulo (en Python un módulo ya es un singleton natural) o
      con inyectar una instancia compartida.
"""

from __future__ import annotations

import threading
from typing import Any, ClassVar


class Singleton:
    """Clase base: cada subclase concreta tiene su propia instancia única."""

    _instances: ClassVar[dict[type, "Singleton"]] = {}
    _lock: ClassVar[threading.Lock] = threading.Lock()

    def __new__(cls, *args: Any, **kwargs: Any) -> "Singleton":
        # Primera comprobación sin lock (camino rápido).
        if cls not in cls._instances:
            with cls._lock:
                # Segunda comprobación: otro hilo pudo crearla mientras esperábamos.
                if cls not in cls._instances:
                    cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]


class Configuration(Singleton):
    """Ejemplo: configuración global de la aplicación."""

    def __init__(self) -> None:
        # __init__ se ejecuta en CADA llamada Configuration(); solo inicializamos
        # la primera vez para no perder los valores ya guardados.
        if not hasattr(self, "_settings"):
            self._settings: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._settings[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)


def demo() -> None:
    a = Configuration()
    b = Configuration()
    a.set("idioma", "es")
    print(f"a is b            -> {a is b}")
    print(f"b.get('idioma')   -> {b.get('idioma')}")

    # Creación concurrente: todos los hilos deben recibir el mismo objeto.
    ids: list[int] = []
    hilos = [threading.Thread(target=lambda: ids.append(id(Configuration()))) for _ in range(8)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    print(f"instancias distintas entre 8 hilos -> {len(set(ids))}")


if __name__ == "__main__":
    demo()
