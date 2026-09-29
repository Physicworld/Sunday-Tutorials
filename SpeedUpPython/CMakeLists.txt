cmake_minimum_required(VERSION 3.12)
project(vector_sum LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Build against the Python interpreter that runs cmake (e.g. the active venv).
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

# Locate pybind11 from the pip package if it is not already visible to cmake.
if(NOT pybind11_DIR)
  execute_process(
    COMMAND "${Python_EXECUTABLE}" -m pybind11 --cmakedir
    OUTPUT_VARIABLE pybind11_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
    ERROR_QUIET)
endif()

# Also look for TBB in the active Python environment (pip package tbb-devel).
get_filename_component(_py_prefix "${Python_EXECUTABLE}" DIRECTORY)
get_filename_component(_py_prefix "${_py_prefix}" DIRECTORY)
list(APPEND CMAKE_PREFIX_PATH "${_py_prefix}")

find_package(TBB REQUIRED)
find_package(pybind11 REQUIRED)

pybind11_add_module(vector_sum vector_sum.cpp)
target_link_libraries(vector_sum PRIVATE TBB::tbb)

# Let the module find libtbb next to the pip install without LD_LIBRARY_PATH.
set_target_properties(vector_sum PROPERTIES
  BUILD_RPATH "${_py_prefix}/lib"
  INSTALL_RPATH "${_py_prefix}/lib")
