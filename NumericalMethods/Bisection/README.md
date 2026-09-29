# Bisección

Método de bisección para hallar raíces de `f(x)` en un intervalo `[a, b]` con `f(a)·f(b) < 0`.

```bash
python Bisection.py --expr 'x**2-2' --a 0 --b 2 --tol 1e-6 [--max-iter 100]
python Bisection.py            # modo interactivo (pregunta función, cotas y tolerancia)
python -m pytest -q            # tests (requiere pytest)
```

Salida: una línea por iteración (`x_a`, `x_b`, punto medio `c`, `f(c)`, iteración) y la raíz. Termina si `|f(c)| < tol` o el semiancho del intervalo es `< tol`; con `--max-iter` agotado o sin cambio de signo en `[a, b]` da un error claro (código de salida 1).

En Python: `bisection(f, a, b, tol=1e-6, max_iter=100)`.

## ¿Por qué no `eval`?

La versión original hacía `eval(texto)` sobre lo que escribía el usuario: `__import__('os').system(...)` habría ejecutado código arbitrario. Aquí la expresión se convierte con `ast` en una lista blanca: variable `x`, números, `+ - * / **`, paréntesis y `sin`, `cos`, `exp`, `log`, `sqrt`. Cualquier otra cosa se rechaza antes de evaluarse. Solo stdlib.
