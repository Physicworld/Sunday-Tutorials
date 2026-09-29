# SpeedUpPython

Suma de vectores en tres versiones para comparar rendimiento:

1. **Python** puro (bucle `for`).
2. **C++ secuencial** (`add_vectors_seq`), expuesto con pybind11.
3. **C++ paralelo** (`add_vectors_par`), con `std::transform(std::execution::par, ...)`.

## Requisitos

- Python 3.9+, `g++` con soporte C++17
- `cmake` >= 3.12, `pybind11`, Intel oneTBB (headers y librería)

`requirements.txt` instala por pip todo lo demás (numpy, matplotlib, pybind11, cmake y `tbb-devel`, que trae TBB con su configuración CMake), así que solo hace falta `g++`. Alternativa con paquetes del sistema (Debian/Ubuntu): `sudo apt install g++ cmake libtbb-dev`.

## Compilar

Desde la raíz del repositorio:

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r SpeedUpPython/requirements.txt
cmake -S SpeedUpPython -B SpeedUpPython/build
cmake --build SpeedUpPython/build -j
```

Genera `SpeedUpPython/build/vector_sum.*.so` (no se versiona). El módulo se compila para el Python que ejecuta cmake, así que activa el venv antes.

## Ejecutar

```bash
cd SpeedUpPython
python compare.py                    # abre el gráfico
MPLBACKEND=Agg python compare.py     # sin ventana (solo tabla)
```

El script comprueba con `np.allclose` que las tres versiones dan el mismo resultado, imprime una tabla de tiempos y dibuja el gráfico (ejes logarítmicos).

## Por qué TBB y no OpenMP

Con GCC, los algoritmos paralelos de la STL (`std::execution::par`, C++17) se apoyan en Intel TBB, no en OpenMP. Por eso `CMakeLists.txt` hace `find_package(TBB REQUIRED)` y enlaza `TBB::tbb`. El código no usa pragmas de OpenMP.

## Interpretar el gráfico

- Para vectores pequeños (~10–1000) el coste fijo de la llamada (y, en la versión paralela, el de arrancar hilos) domina: Python o C++ secuencial pueden ganar.
- Al crecer el tamaño, C++ secuencial supera claramente al bucle de Python, y C++ paralelo se separa del secuencial cuando hay suficiente trabajo por hilo (>= ~10^4–10^5 elementos).
- La suma es limitada por ancho de banda de memoria, así que la aceleración paralela es menor que el número de núcleos.
- Los tiempos son de una sola ejecución: úsalos como orden de magnitud, no como medida precisa.
