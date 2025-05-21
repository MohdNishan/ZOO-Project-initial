cmake_minimum_required(VERSION 3.10)
project(zoo-kernel)

# Set C standard
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

# List source files
set(SOURCES
    service.cpp
    service_internal.cpp
    service_yaml.c
    # service_json.c
    # service_zcfg.c
    # service_callback.c
    # service_conf.c
    # service_storage.c
    # service_map.c
    # service_internal_json.c
    # service_internal_yaml.c
    # zoo_service_loader.c
)


# Find required libraries
find_package(CURL REQUIRED)
find_package(GDAL REQUIRED)
find_package(LibXml2 REQUIRED)


# Add include directories
include_directories(
  ${CURL_INCLUDE_DIRS}
  ${GDAL_INCLUDE_DIR}
  ${LIBXML2_INCLUDE_DIR}
  ${CMAKE_CURRENT_SOURCE_DIR}
)

# Create static library
add_library(zookernel STATIC ${SOURCES})

# Link required libraries
target_link_libraries(zookernel
  ${CURL_LIBRARIES}
  ${GDAL_LIBRARY}
  ${LIBXML2_LIBRARIES}
)
