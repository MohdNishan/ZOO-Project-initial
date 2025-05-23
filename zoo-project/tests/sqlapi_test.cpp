#include <gtest/gtest.h>

// Manually declare the internal functions
extern "C" {
    void* sqlInit();
    void sqlFree(void* handle);
}

TEST(SqlApiTest, SqlInitFree) {
    void* sqlHandle = sqlInit();
    ASSERT_NE(sqlHandle, nullptr);
    sqlFree(sqlHandle);
}
