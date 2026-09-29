"""Patrón Adapter (Estructural).

Problema:
    Tenemos una clase útil cuya interfaz no coincide con la que el cliente
    espera, y no podemos (o no queremos) modificarla.

Solución:
    Crear una clase intermedia (el adaptador) que implementa la interfaz
    esperada y traduce cada llamada a la clase incompatible.

Cuándo usar:
    - Integrar librerías de terceros o código heredado.
    - Reutilizar clases existentes con interfaces distintas.

Cuándo NO usar:
    - Si puedes modificar la clase directamente: cambia su interfaz.
    - Si el "adaptador" acaba reimplementando la lógica: es otro diseño.
"""

from __future__ import annotations

from typing import Protocol


class Temperature(Protocol):
    """Interfaz que espera el cliente: temperatura en grados Celsius."""

    def celsius(self) -> float: ...


class CelsiusSensor:
    """Sensor que ya cumple la interfaz esperada."""

    def __init__(self, value: float) -> None:
        self._value = value

    def celsius(self) -> float:
        return self._value


class LegacyFahrenheitSensor:
    """Clase incompatible (Adaptee): solo sabe dar Fahrenheit."""

    def __init__(self, value: float) -> None:
        self._value = value

    def read_fahrenheit(self) -> float:
        return self._value


class FahrenheitAdapter:
    """Adapter: expone `celsius()` sobre un sensor Fahrenheit."""

    def __init__(self, sensor: LegacyFahrenheitSensor) -> None:
        self._sensor = sensor

    def celsius(self) -> float:
        # Conversión F -> C
        return (self._sensor.read_fahrenheit() - 32) * 5 / 9


def average_celsius(sensors: list[Temperature]) -> float:
    """Código cliente: solo conoce la interfaz `Temperature`."""
    return sum(s.celsius() for s in sensors) / len(sensors)


def demo() -> None:
    sensors: list[Temperature] = [
        CelsiusSensor(20.0),
        FahrenheitAdapter(LegacyFahrenheitSensor(86.0)),  # 30 °C
    ]
    for s in sensors:
        print(f"{type(s).__name__}: {s.celsius():.1f} °C")
    print(f"Promedio: {average_celsius(sensors):.1f} °C")


if __name__ == "__main__":
    demo()
