"""Tests de Temporada 2 (B): Mediator, Visitor, Interpreter."""
import math

import pytest

import interpreter
import mediator
import visitor


def _sala():
    sala = mediator.SalaChat()
    us = [mediator.Usuario(n) for n in ("ana", "luis", "eva")]
    for u in us:
        sala.unirse(u)
    return sala, us


def test_mediator_difunde_a_todos_menos_al_emisor():
    _, (ana, luis, eva) = _sala()
    ana.enviar("hola")
    assert ana.bandeja == []
    assert luis.bandeja == eva.bandeja == ["ana: hola"]


def test_mediator_mensaje_privado_y_errores():
    sala, (ana, luis, eva) = _sala()
    luis.enviar("psst", destino="ana")
    assert ana.bandeja == ["luis: psst"] and eva.bandeja == []
    with pytest.raises(KeyError):
        ana.enviar("x", destino="nadie")
    with pytest.raises(ValueError):
        sala.unirse(mediator.Usuario("ana"))
    with pytest.raises(RuntimeError):
        mediator.Usuario("solo").enviar("hola")


def test_visitor_operaciones_sobre_la_misma_jerarquia():
    figuras = [visitor.Circulo(2), visitor.Rectangulo(2, 3)]
    areas = [f.aceptar(visitor.CalculadorArea()) for f in figuras]
    assert areas == [pytest.approx(math.pi * 4), 6]
    assert [f.aceptar(visitor.ExportadorTexto()) for f in figuras] == [
        "Circulo(radio=2)",
        "Rectangulo(2x3)",
    ]


def test_visitor_es_abstracto():
    with pytest.raises(TypeError):
        visitor.VisitanteFigura()


@pytest.mark.parametrize(
    "texto,esperado",
    [
        ("2 + 3 * 4", 14),
        ("(2 + 3) * 4", 20),
        ("10 - 4 - 3", 3),  # asociatividad a la izquierda
        ("8 / 4 / 2", 1),
        ("1.5 * 2", 3),
    ],
)
def test_interpreter_precedencia_y_asociatividad(texto, esperado):
    assert interpreter.evaluar(texto) == esperado


def test_interpreter_variables():
    assert interpreter.evaluar("x * (y - 1)", x=5, y=3) == 10
    with pytest.raises(NameError):
        interpreter.evaluar("z + 1")


@pytest.mark.parametrize("texto", ["2 +", "(1 + 2", "1 2", "3 $ 4", "__import__('os')"])
def test_interpreter_rechaza_entradas_invalidas(texto):
    with pytest.raises(SyntaxError):
        interpreter.evaluar(texto)


def test_interpreter_division_por_cero():
    with pytest.raises(ZeroDivisionError):
        interpreter.evaluar("1 / 0")
