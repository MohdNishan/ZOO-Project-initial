
cmake_minimum_required(VERSION 3.10)
project(cgic206 C)

# Optional: detect platform
if(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    set(MACOS_CFLAGS "-arch x86_64")
    set(PLATFORM_LIBS /usr/local/lib/libfcgi.dylib)
else()
    set(PLATFORM_LIBS /usr/lib/libfcgi.a)
endif()

# Add flags
if (UNIX)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -I/usr/local/include -g -Wall ${MACOS_CFLAGS}")
endif()

# Library
add_library(cgic STATIC cgic.c)
target_include_directories(cgic PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# Executables
add_executable(cgictest.cgi cgictest.c)
target_link_libraries(cgictest.cgi PRIVATE cgic ${PLATFORM_LIBS})

add_executable(capture capture.c)
target_link_libraries(capture PRIVATE cgic ${PLATFORM_LIBS})

# Optional install (mimics your Makefile)
install(TARGETS cgic ARCHIVE DESTINATION ../../dist/lib)
install(FILES cgic.h DESTINATION ../../dist/include)
