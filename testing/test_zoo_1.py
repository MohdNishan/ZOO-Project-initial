# WPS 1.0



import requests
import xml.etree.ElementTree as ET
from loguru import logger
import unittest
import threading


URL = "http://zookernel/cgi-bin/zoo_loader.cgi"
SERVICE_NAME = "Buffer"


def load_xml(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def modify_xml(file_path, replacements):
    tree = ET.parse(file_path)
    root = tree.getroot()

    namespaces = {
        "wps": "http://www.opengis.net/wps/1.0.0",
        "ows": "http://www.opengis.net/ows/1.1"
    }

    for xpath, new_value in replacements.items():
        element = root.find(xpath, namespaces=namespaces)
        if element is not None:
            element.text = new_value
        else:
            print(f"⚠️ Warning: Element '{xpath}' not found in {file_path}")

    return ET.tostring(root, encoding="utf-8").decode("utf-8")


class TestZOOProjectAPI(unittest.TestCase):


    def send_execute_request(self, file_path):
        """Helper function to send an Execute request"""
        execute_request = load_xml(file_path)
        headers = {"Content-Type": "text/xml"}
        response = requests.post(URL, data=execute_request, headers=headers)
        return response

    # ✅ SUCCESSFUL TESTS
    
    
    
    def test_get_capabilities_success(self):
        """Test successful GetCapabilities request."""
        response = requests.get(f"{URL}?request=GetCapabilities&service=WPS")
        self.assertEqual(response.status_code, 200, "GetCapabilities request failed")
        self.assertIn("wps:Capabilities", response.text, "Invalid GetCapabilities response")
        logger.success("✅ Test Passed: GetCapabilities request successful")


    def test_get_capabilities_multiple_services(self):
        """Test GetCapabilities with multiple service names."""
        response = requests.get(f"{URL}?request=GetCapabilities&service=WPS,WFS")
        self.assertEqual(response.status_code, 400, "Expected failure for multiple services request")
        self.assertIn("InvalidParameterValue", response.text, "Expected error message missing")
        logger.success("✅ Test Passed: GetCapabilities request with multiple services correctly failed")


    def test_concurrent_requests(self):
        """Test concurrent execution of GetCapabilities."""
        def send_request():
            response = requests.get(f"{URL}?request=GetCapabilities&service=WPS")
            self.assertEqual(response.status_code, 200)

        threads = []
        for _ in range(5):
            t = threading.Thread(target=send_request)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        logger.success("✅ Test Passed: Concurrent requests handled correctly") 


    def test_describe_process_success(self):
        """Test successful DescribeProcess request."""
        response = requests.get(f"{URL}?request=DescribeProcess&service=WPS&version=1.0.0&Identifier={SERVICE_NAME}")
        self.assertEqual(response.status_code, 200, "DescribeProcess request failed")
        self.assertIn("wps:ProcessDescriptions", response.text, "Invalid DescribeProcess response")
        logger.success("✅ Test Passed: DescribeProcess request successful")


    def test_execute_process_success(self):
        """Test successful Execute request with valid inputs."""
        try:
            execute_request = load_xml("requests/WPS 1.0/execute_valid.xml")
            headers = {"Content-Type": "text/xml"}
            response = requests.post(URL, data=execute_request, headers=headers)

            self.assertEqual(response.status_code, 200, "ExecuteProcess request failed")
            self.assertIn('"type": "FeatureCollection"', response.text, "Invalid ExecuteProcess response")

            logger.success("✅ Test Passed: ExecuteProcess request successful")
        except Exception as e:
            logger.error(f"❌ Test Failed: {e}")
            self.fail(f"Unexpected error: {e}")


    def test_malformed_xml_request(self):
        """Test ExecuteProcess request with a malformed XML format."""
        malformed_xml = "<wps:Execute xmlns:wps='http://www.opengis.net/wps/1.0.0'><wps:InvalidTag></wps:Execute>"
        headers = {"Content-Type": "text/xml"}
        response = requests.post(URL, data=malformed_xml, headers=headers)
        
        self.assertEqual(response.status_code, 400, "Expected 400 Bad Request for malformed XML")
        self.assertIn("ows:ExceptionReport", response.text, "Malformed XML should return an error")
        logger.success("❌ Test Passed: Malformed XML detected")        


    def test_missing_parameter_in_kvp(self):
        """Test KVP request with a missing required parameter."""
        response = requests.get(f"{URL}?request=DescribeProcess&version=1.0.0") 
        self.assertEqual(response.status_code, 400, "Expected 400 Bad Request for missing parameters")
        logger.success("❌ Test Passed: Missing parameter detected")


    def test_execute_process_async(self):
        """Test asynchronous ExecuteProcess request."""
        try:
            execute_request = load_xml("requests/WPS 1.0/execute_valid_async.xml")
            headers = {"Content-Type": "text/xml"}
            response = requests.post(URL, data=execute_request, headers=headers)

            self.assertEqual(response.status_code, 200, "ExecuteProcess async request failed")
            self.assertIn("<wps:Status", response.text, "Expected asynchronous status response")
            
            logger.success("✅ Test Passed: ExecuteProcess async request successful")
        except Exception as e:
            logger.error(f"❌ Test Failed: {e}")
            self.fail(f"Unexpected error: {e}")


    def test_high_concurrency(self):
        """Test high concurrent execution of GetCapabilities."""
        def send_request():
            response = requests.get(f"{URL}?request=GetCapabilities&service=WPS")
            self.assertEqual(response.status_code, 200)

        threads = []
        for _ in range(50):
            t = threading.Thread(target=send_request)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        logger.success("✅ Test Passed: High concurrency handled correctly") 


    def test_kvp_invalid_request(self):
        """Test KVP request with invalid parameters."""
        response = requests.get(f"{URL}?request=DescribeProcess&service=WPS&wrongparam=value")
        self.assertEqual(response.status_code, 400, "Expected 400 Bad Request for invalid KVP request")
        self.assertIn("ows:ExceptionReport", response.text, "Expected error response missing")
        logger.success("❌ Test Passed: KVP invalid request detected")
    

    def test_kvp_high_load(self):
        """Test KVP requests under high load."""
        def send_request():
            response = requests.get(f"{URL}?request=GetCapabilities&service=WPS")
            self.assertEqual(response.status_code, 200)
    
        threads = []
        for _ in range(10):
            t = threading.Thread(target=send_request)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        logger.success("✅ Test Passed: High load KVP requests handled correctly")


    def test_post_async_high_load(self):
        """Test asynchronous POST ExecuteProcess requests under high load."""
        execute_request = load_xml("requests/WPS 1.0/execute_valid_async.xml")
        headers = {"Content-Type": "text/xml"}

        def send_request():
            response = requests.post(URL, data=execute_request, headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIn("<wps:Status", response.text, "Expected async status response")

        threads = []
        for _ in range(10):
            t = threading.Thread(target=send_request)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        logger.success("✅ Test Passed: POST async requests under load handled correctly")


    def validate_xml_schema(xml_content, schema_url):
        """Validate XML content against a given schema."""
        schema = etree.XMLSchema(etree.parse(schema_url))
        parser = etree.XMLParser(schema=schema)
        
        try:
            etree.fromstring(xml_content.encode("utf-8"), parser)
            logger.success(f"✅ XML validated successfully against schema: {schema_url}")
        except etree.XMLSyntaxError as e:
            logger.error(f"❌ XML Validation Failed: {e}")
            self.fail(f"XML validation error: {e}")


    def test_get_process_list(self):
        """Fetch available processes from GetCapabilities."""
        response = requests.get(f"{URL}?request=GetCapabilities&service=WPS")
        self.assertEqual(response.status_code, 200, "GetCapabilities request failed")
        self.assertIn("wps:Capabilities", response.text, "Invalid GetCapabilities response")
        # print(response.text)
        logger.success("✅ Test Passed: GetCapabilities request successful")



    def test_execute_process_ir_or(self):
        """Test successful Execute request for ir_or."""
        response = self.send_execute_request("requests/WPS 1.0/execute_ir_or.xml")
        self.assertEqual(response.status_code, 200, "ExecuteProcess ir_or request failed")
        logger.success("✅ Test Passed: ExecuteProcess ir_or request successful")
    
    def test_execute_process_irb_o(self):
        """Test successful Execute request for irb_o."""
        response = self.send_execute_request("requests/WPS 1.0/execute_irb_o.xml")
        self.assertEqual(response.status_code, 200, "ExecuteProcess irb_o request failed")
        logger.success("✅ Test Passed: ExecuteProcess irb_o request successful")

    def test_execute_process_irb_or(self):
        """Test successful Execute request for irb_or."""
        response = self.send_execute_request("requests/WPS 1.0/execute_irb_or.xml")
        self.assertEqual(response.status_code, 200, "ExecuteProcess irb_or request failed")
        logger.success("✅ Test Passed: ExecuteProcess irb_or request successful")

    def test_execute_process_ir_or_async(self):
        """Test successful asynchronous Execute request for ir_or_async."""
        response = self.send_execute_request("requests/WPS 1.0/execute_ir_or_async.xml")
        self.assertEqual(response.status_code, 200, "ExecuteProcess ir_or_async request failed")
        logger.success("✅ Test Passed: ExecuteProcess ir_or_async request successful")

    def test_execute_process_irb_o_async(self):
        """Test successful asynchronous Execute request for irb_o_async."""
        response = self.send_execute_request("requests/WPS 1.0/execute_irb_o_async.xml")
        self.assertEqual(response.status_code, 200, "ExecuteProcess irb_o_async request failed")
        logger.success("✅ Test Passed: ExecuteProcess irb_o_async request successful")

    def test_execute_process_irb_or_async(self):
        """Test successful asynchronous Execute request for irb_or_async."""
        response = self.send_execute_request("requests/WPS 1.0/execute_irb_or_async.xml")
        self.assertEqual(response.status_code, 200, "ExecuteProcess irb_or_async request failed")
        logger.success("✅ Test Passed: ExecuteProcess irb_or_async request successful")


    # ❌ ERROR TESTS

    def test_get_capabilities_missing_service(self):
        """Test GetCapabilities request with missing service parameter."""
        response = requests.get(f"{URL}?request=GetCapabilities")
        self.assertEqual(response.status_code, 400, "Expected 400 Bad Request for missing service parameter")
        logger.success("❌ Test Passed: GetCapabilities missing service detected")


    def test_describe_process_invalid_identifier(self):
        """Test DescribeProcess request with an invalid process identifier."""
        response = requests.get(f"{URL}?request=DescribeProcess&service=WPS&version=1.0.0&Identifier=InvalidProcess")
        self.assertEqual(response.status_code, 400, "Expected 400 Bad Request for invalid process identifier")
        self.assertIn("InvalidProcess", response.text, "Expected error message for invalid process identifier")
        logger.success("❌ Test Passed: DescribeProcess invalid identifier detected")


    def test_execute_process_missing_inputs(self):
        """Test ExecuteProcess request with missing required inputs."""
        execute_request = load_xml("requests/WPS 1.0/execute_missing_inputs.xml")
        headers = {"Content-Type": "text/xml"}
        response = requests.post(URL, data=execute_request, headers=headers)

        self.assertEqual(response.status_code, 400, f"Expected 400 Bad Request but got {response.status_code}")
        
        root = ET.fromstring(response.text)
        namespace = {"ows": "http://www.opengis.net/ows/1.1"}
        error_message_element = root.find(".//ows:ExceptionText", namespaces=namespace)
        self.assertIsNotNone(error_message_element, "Expected an error message but none found")

        error_message = error_message_element.text
        expected_message = "The <InputPolygon> argument was not specified"
        self.assertIn(expected_message, error_message, f"Expected error message '{expected_message}' but got '{error_message}'")

        logger.success("❌ Test Passed: ExecuteProcess missing inputs detected")


    def test_execute_process_invalid_input_format(self):
        """Test ExecuteProcess request with an invalid input format."""
        replacements = {
            ".//ows:Identifier": "Buffer",
            ".//wps:LiteralData": "INVALID DATA FORMAT"
        }
        modified_xml = modify_xml("requests/WPS 1.0/execute_invalid_format.xml", replacements)
        # print("Modified XML before sending:\n", modified_xml)
        headers = {"Content-Type": "text/xml"}
        response = requests.post(URL, data=modified_xml, headers=headers)

        self.assertIn(response.status_code, [400, 500], f"Expected 400 or 500 but got {response.status_code}")
        
        root = ET.fromstring(response.text)
        namespace = {"ows": "http://www.opengis.net/ows/1.1"}
        error_message_element = root.find(".//ows:ExceptionText", namespaces=namespace)
        self.assertIsNotNone(error_message_element, "Expected an error message but none found")

        error_message = error_message_element.text
        expected_error_keywords = [
            "Invalid input format",
            "parsing error",
            "invalid parameter",
            "unrecognized value",
            "Unable to open datasource"
        ]
        self.assertTrue(any(keyword in error_message for keyword in expected_error_keywords),
            f"Expected an error message related to invalid input but got: {error_message}")

        logger.success("❌ Test Passed: ExecuteProcess invalid input format detected")