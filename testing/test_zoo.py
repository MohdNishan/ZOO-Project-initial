import requests
import xml.etree.ElementTree as ET
from loguru import logger

logger.add("/app/testing/debug.log", rotation="500 MB", level="DEBUG")

URL = "http://zookernel/cgi-bin/zoo_loader.cgi"
SERVICE_NAME = "Buffer"


def load_xml(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# ✅ SUCCESSFUL TESTS
def test_get_capabilities_success():
    """Test successful GetCapabilities request."""
    response = requests.get(f"{URL}?request=GetCapabilities&service=WPS")
    assert response.status_code == 200, "GetCapabilities request failed"
    assert "wps:Capabilities" in response.text, "Invalid GetCapabilities response"
    logger.success("✅ Test Passed: GetCapabilities request successful")


def test_describe_process_success():
    """Test successful DescribeProcess request."""
    response = requests.get(f"{URL}?request=DescribeProcess&service=WPS&version=1.0.0&Identifier={SERVICE_NAME}")
    assert response.status_code == 200, "DescribeProcess request failed"
    assert "wps:ProcessDescriptions" in response.text, "Invalid DescribeProcess response"
    logger.success("✅ Test Passed: DescribeProcess request successful")


def test_execute_process_success():
    """Test successful Execute request with valid inputs."""
 
    
    try:
        execute_request = load_xml("testing/requests/execute_valid.xml")
        headers = {"Content-Type": "text/xml"}
        response = requests.post(URL, data=execute_request, headers=headers)
   
        assert response.status_code == 200, "ExecuteProcess request failed"
        assert '"type": "FeatureCollection"' in response.text, "Invalid ExecuteProcess response"

        logger.success("✅ Test Passed: ExecuteProcess request successful")
    except Exception as e:
        logger.fail(f"❌ Test Failed: {e}")
        raise


# ❌ ERROR TESTS
def test_get_capabilities_missing_service():
    """Test GetCapabilities request with missing service parameter."""
    response = requests.get(f"{URL}?request=GetCapabilities")
    assert response.status_code == 400, "Expected 400 Bad Request for missing service parameter"
    logger.success("❌ Test Passed: GetCapabilities missing service detected")


def test_describe_process_invalid_identifier():
    """Test DescribeProcess request with an invalid process identifier."""
    response = requests.get(f"{URL}?request=DescribeProcess&service=WPS&version=1.0.0&Identifier=InvalidProcess")
    assert response.status_code == 400, "Expected 400 Bad Request for invalid process identifier"
    assert "InvalidProcess" in response.text, "Expected error message for invalid process identifier"
    logger.success("❌ Test Passed: DescribeProcess invalid identifier detected")


def test_execute_process_missing_inputs():
    """Test ExecuteProcess request with missing required inputs."""
    execute_request = load_xml("testing/requests/execute_missing_inputs.xml")
    headers = {"Content-Type": "text/xml"}
    response = requests.post(URL, data=execute_request, headers=headers)
    # print("Received Response Status Code:", response.status_code)
    # print("Received Response Body:", response.text)
    assert response.status_code == 400, f"Expected 400 Bad Request but got {response.status_code}"
    root = ET.fromstring(response.text)
    namespace = {"ows": "http://www.opengis.net/ows/1.1"}
    error_message_element = root.find(".//ows:ExceptionText", namespaces=namespace)
    assert error_message_element is not None, "Expected an error message but none found"
    error_message = error_message_element.text
    expected_message = "The <InputPolygon> argument was not specified"

    assert expected_message in error_message, f"Expected error message '{expected_message}' but got '{error_message}'"

    logger.success("❌ Test Passed: ExecuteProcess missing inputs detected")


def test_execute_process_invalid_input_format():
    """Test ExecuteProcess request with invalid input format."""
    
    execute_request = load_xml("testing/requests/execute_invalid_format.xml")

    headers = {"Content-Type": "text/xml"}

    response = requests.post(URL, data=execute_request, headers=headers)


    assert response.status_code in [400, 500], f"Expected 400 or 500 but got {response.status_code}"

    root = ET.fromstring(response.text)
    namespace = {"ows": "http://www.opengis.net/ows/1.1"}
    error_message_element = root.find(".//ows:ExceptionText", namespaces=namespace)

    assert error_message_element is not None, "Expected an error message but none found"

    error_message = error_message_element.text


    expected_error_keywords = [
        "Invalid input format",
        "parsing error",
        "invalid parameter",
        "unrecognized value",
        "Unable to open datasource"
    ]

    assert any(keyword in error_message for keyword in expected_error_keywords), \
        f"Expected an error message related to invalid input but got: {error_message}"

    logger.success("❌ Test Passed: ExecuteProcess invalid input format detected")


if __name__ == "__main__":
    # ✅ Successful tests
    test_get_capabilities_success()
    test_describe_process_success()
    test_execute_process_success()

    # ❌ Erroneous tests
    test_get_capabilities_missing_service()
    test_describe_process_invalid_identifier()
    test_execute_process_missing_inputs()
    test_execute_process_invalid_input_format()
