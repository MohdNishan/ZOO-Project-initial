#include <gtest/gtest.h>

extern "C" {
    // Include the API header
    #include "sqlapi.h"

    // Declare missing internal testable functions
    void* sqlInit();
    void sqlFree(void*);
}

TEST(SqlApiTest, InitAndFreeHandle) {
    void* sqlHandle = sqlInit();

    // Ensure initialization was successful
    ASSERT_NE(sqlHandle, nullptr) << "sqlInit() returned null — expected a valid SQLite handle.";

    // Cleanup
    sqlFree(sqlHandle);
}
