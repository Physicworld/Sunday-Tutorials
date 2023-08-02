import sys
sys.path.append('build')

import timeit
import vector_sum
import numpy as np
import matplotlib.pyplot as plt

def python_vector_sum(v1, v2):
    if len(v1) != len(v2):
        raise ValueError('vectors must be the same length')
    
    result = []
    for i in range(len(v1)):
        result.append(v1[i] + v2[i])

    return result

sizes = [10, 100, 1_000, 10_000, 100_000, 1_000_000]

python_times = []
cpp_seq_times = []
cpp_par_times = []

for size in sizes:
    v1 = np.random.rand(size) * 2 - 1
    v2 = np.random.rand(size) * 2 - 1

    # Definimos el tiempo de ejecución de la función de Python
    python_start_time = timeit.default_timer()
    python_vector_sum(v1, v2)
    python_end_time = timeit.default_timer()
    python_times.append(python_end_time - python_start_time)

    # Definimos el tiempo de ejecución de la función de C++ secuencial
    cpp_seq_start_time = timeit.default_timer()
    vector_sum.add_vectors_seq(v1.tolist(), v2.tolist())
    cpp_seq_end_time = timeit.default_timer()
    cpp_seq_times.append(cpp_seq_end_time - cpp_seq_start_time)

    # Definimos el tiempo de ejecución de la función de C++ paralela
    cpp_par_start_time = timeit.default_timer()
    vector_sum.add_vectors_par(v1.tolist(), v2.tolist())
    cpp_par_end_time = timeit.default_timer()
    cpp_par_times.append(cpp_par_end_time - cpp_par_start_time)



plt.figure(figsize=(10, 5))
plt.plot(sizes, cpp_seq_times, 'o-', label='C++ (secuencial)')
plt.plot(sizes, cpp_par_times, 's-', label='C++ (paralelo)')
plt.plot(sizes, python_times, 'd-', label='Python')
plt.xlabel('Vector size')
plt.ylabel('Time (seconds)')
plt.legend()
plt.grid(True)
plt.show()