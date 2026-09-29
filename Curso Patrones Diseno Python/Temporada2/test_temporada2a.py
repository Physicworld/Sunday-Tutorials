"""Tests de Temporada 2 (A): Proxy, Iterator, Template Method, Memento."""
import pytest

import iterator
import memento
import proxy
import template_method


def test_proxy_virtual_es_perezoso_y_cachea():
    proxy.InformeReal.cargas = 0
    p = proxy.InformeVirtualProxy("Q3")
    assert proxy.InformeReal.cargas == 0
    assert p.leer() == p.leer()
    assert proxy.InformeReal.cargas == 1


def test_proxy_proteccion_bloquea_sin_permiso():
    p = proxy.InformeVirtualProxy("Q3")
    with pytest.raises(PermissionError):
        proxy.InformeProteccionProxy(p, "invitado").leer()
    assert "Q3" in proxy.InformeProteccionProxy(p, "admin").leer()


def test_iterator_recorridos():
    p = iterator.Playlist(["A", "B", "C"])
    assert list(p) == ["A", "B", "C"]
    assert list(p) == ["A", "B", "C"]  # se puede recorrer varias veces
    assert list(p.inverso()) == ["C", "B", "A"]
    assert sorted(p.aleatorio(3)) == ["A", "B", "C"]
    assert list(p.aleatorio(3)) == list(p.aleatorio(3))  # semilla determinista


def test_iterator_vacio_y_agotado():
    it = iter(iterator.Playlist([]))
    with pytest.raises(StopIteration):
        next(it)


def test_template_method_orden_fijo_y_hook():
    assert template_method.Te().preparar() == [
        "hervir agua", "infusionar el té 3 minutos", "servir en taza", "añadir limón",
    ]
    sin = template_method.Cafe(con_azucar=False).preparar()
    assert sin == ["hervir agua", "filtrar el café", "servir en taza"]


def test_template_method_es_abstracto():
    with pytest.raises(TypeError):
        template_method.Bebida()


def test_memento_deshacer_restaura_texto_y_cursor():
    ed = memento.Editor()
    h = memento.Historial(ed)
    h.snapshot()
    ed.escribir("Hola")
    h.snapshot()
    ed.escribir(" mundo")
    assert ed.texto == "Hola mundo"
    assert h.deshacer() and (ed.texto, ed.cursor) == ("Hola", 4)
    assert h.deshacer() and (ed.texto, ed.cursor) == ("", 0)
    assert not h.deshacer()


def test_memento_es_inmutable():
    m = memento.Editor().guardar()
    with pytest.raises(Exception):
        m._texto = "x"
