import math
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from Bisection import bisection, parse_expression  # noqa: E402

SCRIPT = Path(__file__).resolve().parent / "Bisection.py"


def test_raiz_de_dos():
    assert bisection(lambda x: x**2 - 2, 0, 2, 1e-6) == pytest.approx(math.sqrt(2), abs=1e-5)


def test_raiz_en_extremo():
    assert bisection(lambda x: x, 0, 1) == 0


def test_sin_cambio_de_signo():
    with pytest.raises(ValueError, match="mismo signo"):
        bisection(lambda x: x**2 + 1, -1, 1)


def test_intervalo_invalido():
    with pytest.raises(ValueError):
        bisection(lambda x: x, 2, 1)


def test_max_iter_agotado():
    with pytest.raises(RuntimeError):
        bisection(lambda x: x - 1 / 3, 0, 1, tol=1e-15, max_iter=3)


def test_expresiones_permitidas():
    f = parse_expression("sin(x)+cos(x)*exp(0)-log(1)+sqrt(4)/2**2-(-x)")
    x = 0.7
    assert f(x) == pytest.approx(math.sin(x) + math.cos(x) + 0.5 + x)


@pytest.mark.parametrize("expr", [
    "__import__('os').system('id')", "open('f')", "x.real", "abs(x)", "sin(x, x)",
    "sin(y)", "y", "'a'", "x if x else 1", "[x]", "lambda: 1", "sin(x=1)", "x+", "",
    "1j", "x**2; 1",
])
def test_expresiones_rechazadas(expr):
    with pytest.raises(ValueError):
        parse_expression(expr)


def test_cli_ok():
    r = subprocess.run([sys.executable, str(SCRIPT), "--expr", "x**2-2", "--a", "0", "--b", "2",
                        "--tol", "1e-6"], capture_output=True, text=True, cwd="/")
    assert r.returncode == 0
    assert "N_iters" in r.stdout and "La raiz buscada es:  1.41" in r.stdout


def test_cli_rechaza_codigo_y_no_ejecuta():
    r = subprocess.run([sys.executable, str(SCRIPT), "--expr", "__import__('os').system('id')",
                        "--a", "0", "--b", "1"], capture_output=True, text=True)
    assert r.returncode == 1 and "uid=" not in r.stdout + r.stderr


def test_cli_sin_cambio_de_signo():
    r = subprocess.run([sys.executable, str(SCRIPT), "--expr", "x**2+1", "--a", "-1", "--b", "1"],
                       capture_output=True, text=True)
    assert r.returncode == 1 and "mismo signo" in r.stderr
