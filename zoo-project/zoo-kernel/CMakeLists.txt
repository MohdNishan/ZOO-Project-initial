cmake_minimum_required(VERSION 3.10)
project(zoo-kernel)

# Set C standard
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

# List source files
set(SOURCES
    service.c
    service_internal.c
    # zoo_service_loader.c
)

# Detect required programs (optional, can be expanded as needed)
find_program(YACC_EXECUTABLE yacc)
find_program(LEX_EXECUTABLE lex)

if(NOT YACC_EXECUTABLE)
  message(WARNING "yacc not found; some features may not be available")
endif()

# Find required libraries
find_package(CURL REQUIRED)
find_library(DL_LIBRARY dl REQUIRED)
find_library(CRYPTO_LIBRARY crypto REQUIRED)
find_library(UUID_LIBRARY uuid REQUIRED)
find_library(JSONC_LIBRARY json-c REQUIRED)

# Find required headers
find_path(CURL_INCLUDE_DIR curl/curl.h REQUIRED)
find_path(CRYPTO_INCLUDE_DIR openssl/evp.h REQUIRED)
find_path(UUID_INCLUDE_DIR uuid/uuid.h REQUIRED)
find_path(JSONC_INCLUDE_DIR json-c/json.h REQUIRED)

# Add include directories
include_directories(
  ${CURL_INCLUDE_DIRS}
  ${CRYPTO_INCLUDE_DIR}
  ${UUID_INCLUDE_DIR}
  ${JSONC_INCLUDE_DIR}
  ${CMAKE_CURRENT_SOURCE_DIR}
)

# Create static library
add_library(zookernel STATIC ${SOURCES})

# Link required libraries
target_link_libraries(zookernel
  ${CURL_LIBRARIES}
  ${DL_LIBRARY}
  ${CRYPTO_LIBRARY}
  ${UUID_LIBRARY}
  ${JSONC_LIBRARY}
)

# Install rules (optional)
install(TARGETS zookernel DESTINATION lib)
install(FILES
  service.h
  service_internal.h
  zoo_service_loader.h
  DESTINATION include
)
