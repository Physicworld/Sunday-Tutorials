"""Observer (Observador).

Problema
    Cuando un objeto cambia, otros deben enterarse, pero no quieres que el
    objeto observado conozca las clases concretas de sus dependientes.

Solución
    El sujeto (``Subject``) mantiene una lista de observadores y expone
    ``subscribe``, ``unsubscribe`` y ``notify``. Cada observador implementa
    ``update`` y se suscribe/desuscribe en tiempo de ejecución.

Cuándo usar
    - Eventos, suscripciones, interfaces reactivas, notificaciones.
    - Una parte del sistema debe reaccionar a cambios de otra sin acoplarse.

Cuándo NO usar
    - Solo hay un dependiente fijo: llámalo directamente.
    - El orden de notificación importa o hay dependencias cíclicas entre
      observadores: se vuelve difícil de razonar y depurar.

Ejemplo didáctico: una estación meteorológica que notifica a pantallas.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Observer(ABC):
    """Interfaz de observador."""

    @abstractmethod
    def update(self, temperature: float) -> None: ...


class Subject:
    """Sujeto observable."""

    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        if observer not in self._observers:  # evita suscripciones duplicadas
            self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, temperature: float) -> None:
        # Se itera sobre una copia: un observador puede desuscribirse al recibir
        for observer in list(self._observers):
            observer.update(temperature)


class WeatherStation(Subject):
    """Sujeto concreto: al medir una nueva temperatura notifica a todos."""

    def __init__(self) -> None:
        super().__init__()
        self.temperature = 0.0

    def set_temperature(self, value: float) -> None:
        self.temperature = value
        self.notify(value)


class Display(Observer):
    """Observador que guarda (e imprime) lo que recibe."""

    def __init__(self, name: str, verbose: bool = False) -> None:
        self.name = name
        self.verbose = verbose
        self.received: list[float] = []

    def update(self, temperature: float) -> None:
        self.received.append(temperature)
        if self.verbose:
            print(f"  [{self.name}] recibió {temperature:.1f} °C")


def demo() -> None:
    station = WeatherStation()
    screen = Display("Pantalla", verbose=True)
    phone = Display("Móvil", verbose=True)
    station.subscribe(screen)
    station.subscribe(phone)

    print("Ambos suscritos:")
    station.set_temperature(21.5)

    station.unsubscribe(phone)
    print("Tras desuscribir el móvil:")
    station.set_temperature(23.0)


if __name__ == "__main__":
    demo()
