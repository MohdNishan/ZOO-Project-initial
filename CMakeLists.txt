cmake_minimum_required(VERSION 3.10)
project(ZOOProject)

<<<<<<< Updated upstream
set(CMAKE_C_STANDARD 99)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/modules")

find_package(Fcgi REQUIRED)

include_directories(${FCGI_INCLUDE_DIRS})

add_subdirectory(thirds/cgic206)
add_subdirectory(zoo-project/zoo-kernel)
=======
#add_subdirectory(zoo-project/zoo-kernel)
add_subdirectory(zoo-project/tests)
>>>>>>> Stashed changes
