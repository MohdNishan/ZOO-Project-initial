cmake_minimum_required(VERSION 3.14)
project(ZooSqlApiTest)


include(FetchContent)

SET(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

macro (ms_link_libraries)
  if(BUILD_DYNAMIC)
    target_link_libraries(sqlapi_test PRIVATE ${ARGV})
  endif(BUILD_DYNAMIC)
  if(BUILD_STATIC)
    target_link_libraries(sqlapi_test_static PRIVATE ${ARGV})
  endif(BUILD_STATIC)
endmacro()

macro( report_optional_not_found component )
  message(SEND_ERROR "${component} library/component/dependency could not be found.
  HINTS:
  - disable ${component} support by adding -DWITH_${component}=0
  - add the ${component} install directory to the CMAKE_PREFIX_PATH variable (-DCMAKE_PREFIX_PATH=\"/path/to/${component}-install-dir;/path/to/other/dirs\"")
endmacro()
macro( report_mandatory_not_found component )
  message(SEND_ERROR "${component} library/component could not be found and is a mandatory dependency
  HINT:
  - add the ${component} install directory to the CMAKE_PREFIX_PATH variable (-DCMAKE_PREFIX_PATH=\"/path/to/${component}-install-dir;/path/to/other/dirs\"")
endmacro()
macro( report_dependency_error component dependency)
  message(SEND_ERROR "${component} support requires ${dependency} support, however ${dependency} support has been disabled.
  HINTS:
  - re-run with -DWITH_${dependency}=1 (or without -DWITH_${dependency}=0)
  - disable ${component} support by adding -DWITH_${component}=0"
  )
endmacro()

# if(WITH_LIBXML2)
  find_package(LibXml2)
  if(LIBXML2_FOUND)
    include_directories(${LIBXML2_INCLUDE_DIR})
    if(NOT DEFINED LIBXML2_LIBRARY)
      set(LIBXML2_LIBRARY ${LIBXML2_LIBRARIES})
    endif()
    # ms_link_libraries( ${LIBXML2_LIBRARY})
    list(APPEND ALL_INCLUDE_DIRS ${LIBXML2_INCLUDE_DIR})
    set (USE_LIBXML2 1)
  else(LIBXML2_FOUND)
    # report_optional_not_found(LIBXML2)
  endif(LIBXML2_FOUND)
# endif (WITH_LIBXML2)


# if(WITH_FCGI)
  find_package(FCGI)
  if(FCGI_FOUND)
    include_directories(${FCGI_INCLUDE_DIR})
    if( NOT FUZZER )
        # target_link_libraries( ${FCGI_LIBRARY})
    endif()
    list(APPEND ALL_INCLUDE_DIRS ${FCGI_INCLUDE_DIR})
    set (USE_FASTCGI 1)
  else(FCGI_FOUND)
    report_optional_not_found(FCGI)
  endif(FCGI_FOUND)
# endif (WITH_FCGI)


find_package(GDAL)
if(NOT GDAL_FOUND)
  report_mandatory_not_found(GDAL)
endif(NOT GDAL_FOUND)

include_directories(${GDAL_INCLUDE_DIR})
# ms_link_libraries( ${GDAL_LIBRARY})
list(APPEND ALL_INCLUDE_DIRS ${GDAL_INCLUDE_DIR})

# Automatically download and configure GoogleTest
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/heads/main.zip
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

enable_testing()

# Add your test executable
add_executable(sqlapi_test sqlapi_test.cpp ../zoo-kernel/service.cpp ../zoo-kernel/sqlapi.cpp ../zoo-kernel/service_internal_gdal.cpp ../zoo-kernel/service_internal.cpp)

# Link it with GoogleTest and your zoo-kernel library (zoo_service)
target_link_libraries(sqlapi_test PRIVATE gtest gtest_main fcgi xml2 gdal)


# Make sure it can find the headers from zoo-kernel
target_include_directories(sqlapi_test PRIVATE
    ${CMAKE_SOURCE_DIR}/zoo-project/zoo-kernel
    ${PROJECT_SOURCE_DIR}/zoo-kernel/usr/include/gdal 
)

# Discover tests
include(GoogleTest)
gtest_discover_tests(sqlapi_test)
