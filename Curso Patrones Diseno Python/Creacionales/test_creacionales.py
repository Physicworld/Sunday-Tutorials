"""Tests de los patrones creacionales. Ejecutar: ``python -m pytest -q test_creacionales.py``."""

from __future__ import annotations

import threading

import pytest

from abstract_factory import DarkFactory, LightFactory, render_form
from builder import ComputerBuilder, Director
from factory_method import Logistics, RoadLogistics, SeaLogistics, Ship, Truck
from prototype import Circle, Rectangle, ShapeRegistry
from singleton import Configuration, Singleton


# --- Singleton ---------------------------------------------------------------


def test_singleton_devuelve_la_misma_instancia() -> None:
    a, b = Configuration(), Configuration()
    assert a is b
    a.set("clave", 1)
    assert b.get("clave") == 1


def test_singleton_una_instancia_con_hilos() -> None:
    Singleton._instances.pop(Configuration, None)  # estado limpio para la prueba
    resultados: list[Configuration] = []
    barrera = threading.Barrier(16)

    def crear() -> None:
        barrera.wait()  # todos los hilos arrancan a la vez
        resultados.append(Configuration())

    hilos = [threading.Thread(target=crear) for _ in range(16)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()

    assert len(resultados) == 16
    assert all(r is resultados[0] for r in resultados)


# --- Prototype ---------------------------------------------------------------


def test_prototype_clon_es_copia_profunda() -> None:
    original = Circle(color="rojo", tags=["base"], radius=2.0)
    clon = original.clone()
    assert clon == original and clon is not original
    clon.tags.append("extra")
    clon.color = "azul"
    assert original.tags == ["base"]
    assert original.color == "rojo"


def test_prototype_registro_entrega_copias_independientes() -> None:
    registro = ShapeRegistry()
    registro.register("rect", Rectangle(color="verde", tags=["t"], width=2, height=3))
    a, b = registro.create("rect"), registro.create("rect")
    assert a is not b and a.tags is not b.tags
    a.tags.append("x")
    assert b.tags == ["t"]


# --- Builder -----------------------------------------------------------------


def test_builder_api_fluida_construye_producto() -> None:
    builder = ComputerBuilder()
    assert builder.with_cpu("x").with_ram(16) is builder  # cada paso devuelve self
    pc = builder.with_gpu("dedicada").build()
    assert (pc.cpu, pc.ram_gb, pc.gpu, pc.storage_gb) == ("x", 16, "dedicada", 256)


def test_builder_falta_campo_obligatorio_lanza_error() -> None:
    with pytest.raises(ValueError, match="ram_gb"):
        ComputerBuilder().with_cpu("x").build()
    with pytest.raises(ValueError, match="cpu"):
        ComputerBuilder().with_ram(8).build()


def test_builder_director_y_producto_inmutable() -> None:
    pc = Director.office_pc(ComputerBuilder())
    assert pc.ram_gb == 8
    with pytest.raises(Exception):
        pc.ram_gb = 64  # type: ignore[misc]  # dataclass congelada


# --- Factory Method ----------------------------------------------------------


def test_factory_method_cada_creador_devuelve_su_producto() -> None:
    assert isinstance(RoadLogistics().create_transport(), Truck)
    assert isinstance(SeaLogistics().create_transport(), Ship)


def test_factory_method_logica_comun_usa_el_producto_de_la_subclase() -> None:
    assert "Camión" in RoadLogistics().plan_delivery("caja")
    assert "Barco" in SeaLogistics().plan_delivery("caja")
    with pytest.raises(TypeError):
        Logistics()  # type: ignore[abstract]  # el creador base es abstracto


# --- Abstract Factory --------------------------------------------------------


@pytest.mark.parametrize("factory,tema", [(LightFactory(), "light"), (DarkFactory(), "dark")])
def test_abstract_factory_familia_coherente(factory, tema) -> None:
    assert factory.create_button().theme == tema
    assert factory.create_checkbox().theme == tema


def test_abstract_factory_las_familias_no_se_mezclan() -> None:
    claro = {type(p) for p in (LightFactory().create_button(), LightFactory().create_checkbox())}
    oscuro = {type(p) for p in (DarkFactory().create_button(), DarkFactory().create_checkbox())}
    assert claro.isdisjoint(oscuro)
    assert render_form(LightFactory()) != render_form(DarkFactory())
