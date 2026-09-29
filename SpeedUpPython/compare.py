"""Benchmark: Python loop vs C++ sequential vs C++ parallel (TBB) vector sum."""
import sys
import timeit
from pathlib import Path

import numpy as np

# The compiled module lives in ./build (see README.md), regardless of the cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent / "build"))

try:
    import vector_sum
except ImportError as exc:
    sys.exit(
        f"Cannot import the compiled 'vector_sum' module ({exc}).\n"
        "Build it first: cmake -S SpeedUpPython -B SpeedUpPython/build "
        "&& cmake --build SpeedUpPython/build -j"
    )

import matplotlib.pyplot as plt


def python_vector_sum(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("v1 and v2 must be the same length")

    result = []
    for i in range(len(v1)):
        result.append(v1[i] + v2[i])

    return result


def timed(func, *args):
    start = timeit.default_timer()
    result = func(*args)
    return result, timeit.default_timer() - start


sizes = [10, 100, 1_000, 10_000, 100_000, 1_000_000]

python_times = []
cpp_seq_times = []
cpp_par_times = []

rng = np.random.default_rng(0)

for size in sizes:
    v1 = rng.uniform(-1, 1, size)
    v2 = rng.uniform(-1, 1, size)

    py_result, t = timed(python_vector_sum, v1, v2)
    python_times.append(t)
    seq_result, t = timed(vector_sum.add_vectors_seq, v1, v2)
    cpp_seq_times.append(t)
    par_result, t = timed(vector_sum.add_vectors_par, v1, v2)
    cpp_par_times.append(t)

    if not (np.allclose(py_result, seq_result) and np.allclose(py_result, par_result)):
        sys.exit(f"Results differ between implementations for size {size}")

print(f"{'size':>10} {'python (s)':>12} {'C++ seq (s)':>12} {'C++ par (s)':>12}")
for row in zip(sizes, python_times, cpp_seq_times, cpp_par_times):
    print(f"{row[0]:>10} {row[1]:>12.6f} {row[2]:>12.6f} {row[3]:>12.6f}")
print("Results match across Python, C++ sequential and C++ parallel.")

plt.figure(figsize=(10, 6))
plt.plot(sizes, cpp_seq_times, 'o-', label='C++ sequential')
plt.plot(sizes, cpp_par_times, 's-', label='C++ parallel')
plt.plot(sizes, python_times, 'd-', label='Python')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Vector size')
plt.ylabel('Time (seconds)')
plt.grid(True)
plt.legend()
plt.show()
