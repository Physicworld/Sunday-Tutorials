#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <algorithm>
#include <execution>

namespace py = pybind11;

py::array_t<double> add_vectors_seq(py::array_t<double> arr1, py::array_t<double> arr2) {
    auto r1 = arr1.unchecked<1>();
    auto r2 = arr2.unchecked<1>();
    size_t n = arr1.size();
    auto result = py::array_t<double>(n);
    auto r = result.mutable_unchecked<1>();

    for(size_t i = 0; i < n; i++) {
        r[i] = r1[i] + r2[i];
    }

    return result;
}

py::array_t<double> add_vectors_par(py::array_t<double> arr1, py::array_t<double> arr2) {
    auto r1 = arr1.unchecked<1>();
    auto r2 = arr2.unchecked<1>();
    size_t n = arr1.size();
    auto result = py::array_t<double>(n);
    auto r = result.mutable_unchecked<1>();

    std::transform(std::execution::par, r1.data(0), r1.data(0) + n, r2.data(0), r.mutable_data(0), std::plus<>());

    return result;
}

PYBIND11_MODULE(vector_sum, m) {
    m.def("add_vectors_seq", &add_vectors_seq, "Add two vectors sequentially");
    m.def("add_vectors_par", &add_vectors_par, "Add two vectors in parallel");
}
