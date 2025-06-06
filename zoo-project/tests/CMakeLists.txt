cmake_minimum_required(VERSION 3.14)
project(zoo-project-test LANGUAGES C CXX)

set(ZOO_LIB_TARGET_NAME zoo_service)


option(WITH_AMQP "Enable AMQP messaging for asynchrnous tasks execution" OFF)
option(WITH_DRU "Enable OGC API - Processes - Part 2: Deploy, Replace, Undeploy )" OFF)


include(FetchContent)

set(CMAKE_CXX_STANDARD 17
  CACHE STRING "C++ standard version to use (default is 17)")
message(STATUS "Requiring C++${CMAKE_CXX_STANDARD}")
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(BUILD_DYNAMIC 1)
message(STATUS "Requiring C++${CMAKE_CXX_STANDARD} - done")


SET(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

macro (zoo_link_libraries)
  if(BUILD_DYNAMIC)
    target_link_libraries(ZOO_Service_Shared_Library PRIVATE ${ARGV})
  endif(BUILD_DYNAMIC)
  if(BUILD_STATIC)
    target_link_libraries(ZOO_Service_Shared_Library_static PRIVATE ${ARGV})
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
    # zoo_link_libraries( ${LIBXML2_LIBRARY})
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

find_package(JSONC)
if(JSONC_FOUND)
  message(STATUS "JSONC Include Dir: ${JSONC_INCLUDE_DIRS}")
  list(APPEND ALL_INCLUDE_DIRS ${JSONC_INCLUDE_DIRS})
  include_directories(${JSONC_INCLUDE_DIRS})
endif(JSONC_FOUND)

find_package(UUID)
if(UUID_FOUND)
  message(STATUS "UUID Include Dir: ${UUID_INCLUDE_DIR}")
  list(APPEND ALL_INCLUDE_DIRS ${UUID_INCLUDE_DIR})
  include_directories(${UUID_INCLUDE_DIR})
endif(UUID_FOUND)


find_package(LibXslt)
if(LIBXSLT_FOUND)
  if(NOT DEFINED LIBXSLT_LIBRARY)
    set(LIBXSLT_LIBRARY ${LIBXSLT_LIBRARIES})
  endif()
  include_directories(${LIBXSLT_INCLUDE_DIR})
  #ms_link_libraries( ${LIBXSLT_LIBRARY} ${LIBXSLT_EXSLT_LIBRARY})
  list(APPEND ALL_INCLUDE_DIRS ${LIBXSLT_INCLUDE_DIR})
  set(USE_XMLMAPFILE 1)
else(LIBXSLT_FOUND)
  message(SEND_ERROR "Xml Mapfile support requires XSLT support which was not found.
  HINTS:
  - add the libxslt install directory to the CMAKE_PREFIX_PATH variable (-DCMAKE_PREFIX_PATH=\"/path/to/libxslt-install-dir;/path/to/other/dirs\"
  - disable Xml Mapfile support by adding -DWITH_XMLMAPFILE=0"
  )
endif(LIBXSLT_FOUND)


find_package(GDAL)
if(NOT GDAL_FOUND)
  report_mandatory_not_found(GDAL)
endif(NOT GDAL_FOUND)

include_directories(${GDAL_INCLUDE_DIR})
# zoo_link_libraries( ${GDAL_LIBRARY})
list(APPEND ALL_INCLUDE_DIRS ${GDAL_INCLUDE_DIR})

# Automatically download and configure GoogleTest
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/heads/main.zip
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

set( ZOO_LOG_FORMAT "%d | %l | %p %f:%u:%i - %m")

enable_testing()

include_directories(../../../thirds/cgic206)

# Add your test executable
#add_executable(ZOO_Service_Shared_Library sqlapi_test.cpp ../zoo-kernel/service.cpp ../zoo-kernel/service_internal_gdal.cpp ../zoo-kernel/sqlapi.cpp )
add_executable(ZOO_Service_Shared_Library 
  sqlapi_test.cpp 
  ../zoo-kernel/service.cpp 
  ../zoo-kernel/service_internal_gdal.cpp 
  ../zoo-kernel/sqlapi.cpp 
  ../zoo-kernel/service_internal.c
  ../zoo-kernel/request_parser.cpp
  ../zoo-kernel/caching.cpp
  ../zoo-kernel/response_print.cpp
  ../zoo-kernel/server_internal.cpp
  ../zoo-kernel/service_callback.cpp
  ../zoo-kernel/ulinet.c
  ../zoo-kernel/service_json.cpp
  ../zoo-kernel/zoo_loader.cpp
  ../../../thirds/cgic206/cgic.c
)


add_definitions(-DUSE_AMQP=1)
add_definitions(-DMETA_DB=1)
add_definitions(-DRELY_ON_DB=1)
add_definitions(-DDRU_ENABLED=1)
add_definitions(-DPROJ_VERSION_MAJOR=8)
add_definitions(-DZOO_VERSION="1.8.0")

# Link it with GoogleTest and your zoo-kernel library (zoo_service)
#target_link_libraries(zoo_service PRIVATE fcgi xml2 gdal curl crypto uuid json-c)

target_link_libraries(ZOO_Service_Shared_Library PRIVATE gtest gtest_main fcgi xml2 gdal curl crypto uuid json-c ${CMAKE_THREAD_LIBS_INIT} ${CURL_LIBRARIES}
    ${LIBXML2_LIBRARIES} ${CGIC_LIBRARY}
    pthread )

find_package(BISON REQUIRED)
find_package(FLEX REQUIRED)

# Process main_conf_read.l and main_conf_read.y from zoo-kernel directory
BISON_TARGET(MainConfReadParser
    ../zoo-kernel/main_conf_read.y
    ${CMAKE_CURRENT_BINARY_DIR}/main_conf_read.tab.c
)
FLEX_TARGET(MainConfReadScanner
    ../zoo-kernel/main_conf_read.l
    ${CMAKE_CURRENT_BINARY_DIR}/main_conf_read.yy.c
)
ADD_FLEX_BISON_DEPENDENCY(MainConfReadScanner MainConfReadParser)



# Make sure it can find the headers from zoo-kernel
target_include_directories(ZOO_Service_Shared_Library PRIVATE
    ${CMAKE_SOURCE_DIR}/thirds/cgic206
    ${CMAKE_SOURCE_DIR}/zoo-project/zoo-kernel
    ${PROJECT_SOURCE_DIR}/zoo-kernel/usr/include/gdal 
    ${CMAKE_CURRENT_BINARY_DIR}
)

# Add the parser+scanner source files and your config loader
set(CONF_SRC
    ${BISON_MainConfReadParser_OUTPUTS}
    ${FLEX_MainConfReadScanner_OUTPUTS}
    loadLocalCfg.cpp
)

# Discover tests
include(GoogleTest)

gtest_discover_tests(ZOO_Service_Shared_Library)
 