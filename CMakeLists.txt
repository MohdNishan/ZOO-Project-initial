cmake_minimum_required(VERSION 3.10)
project(ZOOProject)

set(CMAKE_C_STANDARD 99)

# Add custom CMake module path
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/modules")

# Find FastCGI
find_package(Fcgi REQUIRED)

# Include FCGI headers
include_directories(${FCGI_INCLUDE_DIRS})

# Add subdirectory for cgic
add_subdirectory(thirds/cgic206)
