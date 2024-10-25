cmake_minimum_required(VERSION 3.20)
project(hello)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")
add_executable(hello hello.cpp)