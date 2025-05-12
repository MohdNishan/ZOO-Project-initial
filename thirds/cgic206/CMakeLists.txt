cmake_minimum_required(VERSION 3.10)

set(CMAKE_C_STANDARD 99)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/../../cmake/modules")

include_directories(${FCGI_INCLUDE_DIRS})

cmake_minimum_required(VERSION 3.10)
project(cgic206 C)

find_package(Fcgi REQUIRED)

if (UNIX)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -g -Wall")
endif()

add_library(cgic STATIC cgic.c)
target_include_directories(cgic PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(cgictest.cgi cgictest.c)
target_include_directories(cgictest.cgi PRIVATE ${FCGI_INCLUDE_DIRS})
target_link_libraries(cgictest.cgi PRIVATE cgic ${FCGI_LIBRARIES})

add_executable(capture capture.c)
target_include_directories(capture PRIVATE ${FCGI_INCLUDE_DIRS})
target_link_libraries(capture PRIVATE cgic ${FCGI_LIBRARIES})

install(TARGETS cgic ARCHIVE DESTINATION ../../dist/lib)
install(FILES cgic.h DESTINATION ../../dist/include)

