cmake_minimum_required(VERSION 3.10)
project(zoo-kernel)

# Specify source files
set(SOURCES
    service.c
    service_internal.c
    zoo_service_loader.c
)

# Include headers
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# Create a static library
add_library(zookernel STATIC ${SOURCES})
