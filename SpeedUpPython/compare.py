import sys
sys.path.append('build')

import timeit
import numpy as np
import vector_sum
import matplotlib.pyplot as plt

def python_vector_sum(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("v1 and v2 must be the same length")
    
    result = []
    for i in range(len(v1)):
        result.append(v1[i] + v2[i])
    
    return result


sizes = [10, 100, 1000, 10000, 100000, 1000000]

python_times = []
c_seq_times = []
c_par_times = []

for size in sizes:
    # Definir vectores aleatorios
    v1 = np.random.rand(size)
    v2 = np.random.rand(size)

    # Definir el tiempo de ejecución de la funcion de python
    python_start_time = timeit.default_timer()
    python_vector_sum(v1, v2)
    python_end_time = timeit.default_timer()
    python_times.append(python_end_time - python_start_time)

    # Definir el tiempo de ejecución de la funcion de C secuencial
    c_seq_start_time = timeit.default_timer()
    vector_sum.add_vectors_seq(v1, v2)
    c_seq_end_time = timeit.default_timer()
    c_seq_times.append(c_seq_end_time - c_seq_start_time)

    # Definir el tiempo de ejecución de la funcion de C paralela
    c_par_start_time = timeit.default_timer()
    vector_sum.add_vectors_par(v1, v2)
    c_par_end_time = timeit.default_timer()
    c_par_times.append(c_par_end_time - c_par_start_time)



plt.figure(figsize=(10, 6))
plt.plot(sizes, c_seq_times, 'o-', label='C sequential')
plt.plot(sizes, c_par_times, 's-', label='C parallel')
plt.plot(sizes, python_times, 'd-', label='Python')
plt.xlabel('Vector size')
plt.ylabel('Time (seconds)')
plt.legend()
plt.show()
