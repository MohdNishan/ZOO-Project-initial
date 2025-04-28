cmake_minimum_required(VERSION 3.10)
project(ZOOProjectTests)

# Enable testing
enable_testing()

# Add GoogleTest
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/release-1.12.1.zip
)
FetchContent_MakeAvailable(googletest)

# Add test executable
add_executable(kernel_test tests/kernel_test.cpp)

# Link GoogleTest and GoogleTestMain
target_link_libraries(kernel_test gtest gtest_main)

# Add test to CTest
include(GoogleTest)
gtest_discover_tests(kernel_test)
