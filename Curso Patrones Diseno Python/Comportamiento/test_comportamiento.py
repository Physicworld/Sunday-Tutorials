"""Tests pytest de los patrones de Comportamiento (invariante clave de cada uno)."""

import pytest

from chain_of_responsibility import CEO, Director, Handler, Manager, build_chain
from command import DeleteCommand, Invoker, TextEditor, WriteCommand
from observer import Display, WeatherStation
from state import InvalidTransition, Order
from strategy import FixedDiscount, PercentageDiscount, ShoppingCart


# --- Chain of Responsibility -------------------------------------------------
def test_chain_respeta_el_orden_de_los_handlers():
    chain = build_chain()
    assert chain.handle(500) == "Manager aprobó 500"
    assert chain.handle(5_000) == "Director aprobó 5,000"
    assert chain.handle(50_000) == "CEO aprobó 50,000"


def test_chain_peticion_no_manejada_devuelve_none():
    assert build_chain().handle(1_000_000) is None


def test_chain_reordenar_cambia_quien_atiende():
    ceo: Handler = CEO()
    ceo.set_next(Manager())
    assert ceo.handle(10).startswith("CEO")  # el primero que puede, gana
    solo_manager = Manager()
    solo_manager.set_next(Director())
    assert solo_manager.handle(2_000).startswith("Director")


# --- Command -----------------------------------------------------------------
def test_command_undo_en_orden_inverso():
    editor, invoker = TextEditor(), Invoker()
    invoker.run(WriteCommand(editor, "Hola"))
    invoker.run(WriteCommand(editor, " mundo"))
    invoker.run(DeleteCommand(editor, 3))
    assert editor.text == "Hola mu"
    invoker.undo()
    assert editor.text == "Hola mundo"
    invoker.undo()
    assert editor.text == "Hola"
    invoker.undo()
    assert editor.text == ""


def test_command_undo_sin_historial_devuelve_false():
    invoker = Invoker()
    assert invoker.undo() is False
    invoker.run(WriteCommand(TextEditor(), "x"))
    assert invoker.history_size == 1
    assert invoker.undo() is True
    assert invoker.history_size == 0


# --- Observer ----------------------------------------------------------------
def test_observer_notifica_a_todos_los_suscritos():
    station, a, b = WeatherStation(), Display("a"), Display("b")
    station.subscribe(a)
    station.subscribe(b)
    station.set_temperature(20.0)
    assert a.received == [20.0]
    assert b.received == [20.0]


def test_observer_removido_no_recibe_mas_notificaciones():
    station, a, b = WeatherStation(), Display("a"), Display("b")
    station.subscribe(a)
    station.subscribe(b)
    station.set_temperature(1.0)
    station.unsubscribe(b)
    station.set_temperature(2.0)
    assert a.received == [1.0, 2.0]
    assert b.received == [1.0]


def test_observer_suscripcion_duplicada_notifica_una_vez():
    station, a = WeatherStation(), Display("a")
    station.subscribe(a)
    station.subscribe(a)
    station.set_temperature(5.0)
    assert a.received == [5.0]


# --- State -------------------------------------------------------------------
def test_state_transiciones_validas():
    order = Order()
    assert order.status == "Pending"
    order.pay()
    assert order.status == "Paid"
    order.ship()
    assert order.status == "Shipped"
    order.deliver()
    assert order.status == "Delivered"


def test_state_transiciones_invalidas_lanzan_error():
    order = Order()
    with pytest.raises(InvalidTransition):
        order.ship()  # no se envía sin pagar
    assert order.status == "Pending"  # el estado no cambia tras el error
    order.pay()
    order.ship()
    with pytest.raises(InvalidTransition):
        order.cancel()  # no se cancela tras enviar


def test_state_cancelled_es_estado_final():
    order = Order()
    order.cancel()
    assert order.status == "Cancelled"
    with pytest.raises(InvalidTransition):
        order.pay()


# --- Strategy ----------------------------------------------------------------
def test_strategy_intercambio_en_tiempo_de_ejecucion():
    cart = ShoppingCart()
    cart.add(100.0)
    assert cart.total() == 100.0
    cart.set_strategy(PercentageDiscount(10))
    assert cart.total() == pytest.approx(90.0)
    cart.set_strategy(FixedDiscount(25))
    assert cart.total() == pytest.approx(75.0)


def test_strategy_descuento_fijo_nunca_deja_total_negativo():
    cart = ShoppingCart(FixedDiscount(500))
    cart.add(10.0)
    assert cart.total() == 0.0
