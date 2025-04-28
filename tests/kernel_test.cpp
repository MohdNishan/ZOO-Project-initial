#include <gtest/gtest.h>

// Sample function to test
int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}

int multiply(int a, int b) {
    return a * b;
}

int divide(int a, int b) {
    if (b == 0) throw std::invalid_argument("Division by zero");
    return a / b;
}

TEST(ZooKernelTest, Addition) {
    EXPECT_EQ(add(2, 3), 5);
    EXPECT_EQ(add(-1, 1), 0);
}

TEST(ZooKernelTest, Subtraction) {
    EXPECT_EQ(subtract(5, 3), 2);
    EXPECT_EQ(subtract(2, 4), -2);
}

TEST(ZooKernelTest, Multiplication) {
    EXPECT_EQ(multiply(3, 4), 12);
    EXPECT_EQ(multiply(-2, 5), -10);
}

TEST(ZooKernelTest, Division) {
    EXPECT_EQ(divide(10, 2), 5);
    EXPECT_THROW(divide(5, 0), std::invalid_argument);
}
