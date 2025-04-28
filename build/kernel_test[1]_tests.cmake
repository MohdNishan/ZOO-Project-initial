add_test([=[ZooKernelTest.Addition]=]  [==[C:/Users/Mhd Nishan/Desktop/zoo-project/ZOO-Project/build/Debug/kernel_test.exe]==] [==[--gtest_filter=ZooKernelTest.Addition]==] --gtest_also_run_disabled_tests)
set_tests_properties([=[ZooKernelTest.Addition]=]  PROPERTIES WORKING_DIRECTORY [==[C:/Users/Mhd Nishan/Desktop/zoo-project/ZOO-Project/build]==] SKIP_REGULAR_EXPRESSION [==[\[  SKIPPED \]]==])
set(  kernel_test_TESTS ZooKernelTest.Addition)
