# WPS 2.0



import requests
import xml.etree.ElementTree as ET
from loguru import logger
import unittest

logger.add("/app/testing/debug.log", rotation="500 MB", level="DEBUG")

URL = "http://zookernel/cgi-bin/zoo_loader.cgi"
SERVICE_NAME = "Buffer"

def load_xml(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

class TestZOOProjectAPI_WPS2(unittest.TestCase):

    def send_execute_request(self, file_path):
        """Helper function to send an Execute request"""
        execute_request = load_xml(file_path)
        headers = {"Content-Type": "text/xml"}
        response = requests.post(URL, data=execute_request, headers=headers)
        return response

    def test_get_capabilities_success(self):
        """Test successful GetCapabilities request for WPS 2.0."""
        response = requests.get(f"{URL}?request=GetCapabilities&service=WPS&version=2.0.0")
        self.assertEqual(response.status_code, 200, "GetCapabilities request failed")
        self.assertIn("wps:Capabilities", response.text, "Invalid GetCapabilities response")
        logger.success("✅ Test Passed: GetCapabilities request successful")

    def test_describe_process_success(self):
        """Test successful DescribeProcess request for WPS 2.0."""
        response = requests.get(f"{URL}?request=DescribeProcess&service=WPS&version=2.0.0&Identifier={SERVICE_NAME}")
        self.assertEqual(response.status_code, 200, "DescribeProcess request failed")
        self.assertIn("wps:ProcessOfferings", response.text, "Invalid DescribeProcess response")
        logger.success("✅ Test Passed: DescribeProcess request successful")

    def test_execute_process(self):
        """Test successful Execute requests for multiple processes in WPS 2.0."""
        test_cases = [
            "execute_ir_or.xml",
            "execute_irb_o.xml",
            "execute_irb_or.xml",
            "execute_ir_or_async.xml",
            "execute_irb_o_async.xml",
            "execute_irb_or_async.xml"
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                response = self.send_execute_request(f"testing/requests/{test_case}")
                self.assertEqual(response.status_code, 200, f"ExecuteProcess {test_case} request failed")
                logger.success(f"✅ Test Passed: ExecuteProcess {test_case} request successful")

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    result = runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(TestZOOProjectAPI_WPS2))

    total_tests = result.testsRun
    failed_tests = len(result.failures) + len(result.errors)
    successful_tests = total_tests - failed_tests

    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

    print("\\n=================== TEST REPORT WPS 2.0 ===================")
    print(f"✅ Successful Tests: {successful_tests}{RESET}")
    print(f"❌ Failed Tests: {failed_tests}{RESET}")
    print(f"📊 Total Tests Ran: {total_tests}")
    print("=============================================================\n")

    if failed_tests > 0:
        print(f"{RED}❗ Some tests failed. Check logs above for details.{RESET}")
        print("\nFailed Tests:")
        for failed_test, traceback in result.failures + result.errors:
            print(f"🔴 {failed_test.id()}")
    else:
        print(f"{GREEN}🎉 All tests passed successfully!{RESET}")
