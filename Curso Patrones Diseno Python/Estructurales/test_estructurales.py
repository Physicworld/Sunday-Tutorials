"""Tests de los patrones estructurales."""

import pytest

import adapter
import bridge
import composite
import decorator
import facade
import flyweight


def test_adapter_satisfies_expected_interface():
    sensors = [adapter.CelsiusSensor(20.0), adapter.FahrenheitAdapter(adapter.LegacyFahrenheitSensor(86.0))]
    assert sensors[1].celsius() == pytest.approx(30.0)
    assert adapter.average_celsius(sensors) == pytest.approx(25.0)


def test_bridge_combinations_are_independent():
    for remote_cls in (bridge.RemoteControl, bridge.AdvancedRemoteControl):
        for device_cls in (bridge.Tv, bridge.Radio):
            device = device_cls()
            remote = remote_cls(device)
            assert remote.toggle_power().startswith(device.name())
            assert device.on is True
    device = bridge.Radio()
    assert bridge.AdvancedRemoteControl(device).mute() == "Radio en silencio"
    assert device.volume == 0


def test_composite_uniform_total():
    leaf = composite.Product("a", 5.0)
    tree = composite.Box("b").add(leaf).add(composite.Box("c").add(composite.Product("d", 7.0)))
    assert leaf.total() == 5.0
    assert tree.total() == 12.0


def test_decorator_stacking_and_order():
    drink = decorator.Sugar(decorator.Milk(decorator.Coffee()))
    assert drink.cost() == pytest.approx(2.7)
    assert drink.description() == "Café + leche + azúcar"
    other = decorator.Milk(decorator.Sugar(decorator.Coffee()))
    assert other.description() == "Café + azúcar + leche"


def test_decorator_function_order_and_wraps():
    # @shout sobre @exclaim: primero '!' y luego mayúsculas
    assert decorator.greet("x") == "HOLA X!"
    assert decorator.greet.__name__ == "greet"
    assert decorator.greet.__doc__ == "Saluda a `name`."


def test_facade_orchestrates_in_order():
    log = facade.HomeTheaterFacade().watch_movie("Peli")
    assert log == [
        "Amplifier: encendido",
        "Projector: encendido",
        "Projector: entrada HDMI",
        "Player: reproduciendo Peli",
    ]


def test_flyweight_shares_intrinsic_state():
    flyweight.TreeTypeFactory.clear()
    a = flyweight.TreeTypeFactory.get("Pino", "verde", "lisa")
    b = flyweight.TreeTypeFactory.get("Pino", "verde", "lisa")
    assert a is b
    flyweight.TreeTypeFactory.get("Roble", "verde", "lisa")
    assert flyweight.TreeTypeFactory.count() == 2
    t1, t2 = flyweight.Tree(1, 1, a), flyweight.Tree(2, 2, b)
    assert t1.type is t2.type
    flyweight.TreeTypeFactory.clear()
