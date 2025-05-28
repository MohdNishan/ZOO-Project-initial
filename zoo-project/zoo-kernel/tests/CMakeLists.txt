cmake_minimum_required(VERSION 3.10)
project(ZooSqlApiTests)

# Enable CTest support
enable_testing()

# Find and include GoogleTest
find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})

# Include ZOO-Project kernel headers
include_directories(../zoo-kernel)

# Link to ZOO-Project kernel build output (assuming the zoo_service lib is built there)
link_directories(${CMAKE_BINARY_DIR}/zoo-kernel)

# Define the test executable
add_executable(sqlapi_test sqlapi_test.cpp)

# Link libraries: GTest, pthread, and zoo_service
target_link_libraries(sqlapi_test ${GTEST_LIBRARIES} pthread zoo_service)

# Register the test with CTest
add_test(NAME SqlApiTest COMMAND sqlapi_test)
