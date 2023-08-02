cmake_minimum_required(VERSION 3.12)
project(vector_sum)

set(CMAKE_CXX_STANDARD 17)

find_package(TBB REQUIRED)

find_package(pybind11 REQUIRED)

pybind11_add_module(vector_sum vector_sum.cpp)

target_link_libraries(vector_sum PRIVATE TBB::tbb)