"""Patrón Bridge (Estructural).

Problema:
    Dos dimensiones que varían de forma independiente (p. ej. tipo de mando y
    tipo de dispositivo) provocan una explosión de subclases (N x M).

Solución:
    Separar la abstracción de la implementación en dos jerarquías y
    conectarlas por composición: la abstracción delega en un implementador.

Cuándo usar:
    - Cuando ambas jerarquías deben poder extenderse por separado.
    - Cuando quieres cambiar la implementación en tiempo de ejecución.

Cuándo NO usar:
    - Si solo hay una dimensión de variación: una jerarquía simple basta.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Device(ABC):
    """Implementor: API de bajo nivel de un dispositivo."""

    def __init__(self) -> None:
        self.on = False
        self.volume = 10

    @abstractmethod
    def name(self) -> str: ...


class Tv(Device):
    def name(self) -> str:
        return "TV"


class Radio(Device):
    def name(self) -> str:
        return "Radio"


class RemoteControl:
    """Abstraction: mando básico que delega en un `Device`."""

    def __init__(self, device: Device) -> None:
        self.device = device

    def toggle_power(self) -> str:
        self.device.on = not self.device.on
        return f"{self.device.name()} {'encendida' if self.device.on else 'apagada'}"


class AdvancedRemoteControl(RemoteControl):
    """Abstracción refinada: añade `mute` sin tocar los dispositivos."""

    def mute(self) -> str:
        self.device.volume = 0
        return f"{self.device.name()} en silencio"


def demo() -> None:
    # Cualquier mando se combina con cualquier dispositivo (2 x 2 sin 4 clases).
    for remote_cls in (RemoteControl, AdvancedRemoteControl):
        for device_cls in (Tv, Radio):
            remote = remote_cls(device_cls())
            line = f"{remote_cls.__name__} + {device_cls.__name__}: {remote.toggle_power()}"
            if isinstance(remote, AdvancedRemoteControl):
                line += f", {remote.mute()}"
            print(line)


if __name__ == "__main__":
    demo()
