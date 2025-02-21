import requests
import xml.etree.ElementTree as ET
from loguru import logger

logger.add("/app/testing/debug.log", rotation="500 MB", level="DEBUG")

URL = "http://zookernel/cgi-bin/zoo_loader.cgi"
SERVICE_NAME = "Buffer"


# ✅ SUCCESSFUL TESTS
def test_get_capabilities_success():
    """Test successful GetCapabilities request."""
    response = requests.get(f"{URL}?request=GetCapabilities&service=WPS")
    assert response.status_code == 200, "GetCapabilities request failed"
    assert "wps:Capabilities" in response.text, "Invalid GetCapabilities response"
    print("✅ Test Passed: GetCapabilities request successful")


def test_describe_process_success():
    """Test successful DescribeProcess request."""
    response = requests.get(f"{URL}?request=DescribeProcess&service=WPS&version=1.0.0&Identifier={SERVICE_NAME}")
    assert response.status_code == 200, "DescribeProcess request failed"
    assert "wps:ProcessDescriptions" in response.text, "Invalid DescribeProcess response"
    print("✅ Test Passed: DescribeProcess request successful")


def test_execute_process_success():
    """Test successful Execute request with valid inputs."""
    execute_request = f"""<wps:Execute xmlns:wps="http://www.opengis.net/wps/1.0.0"
                 xmlns:ows="http://www.opengis.net/ows/1.1"
                 xmlns:xlink="http://www.w3.org/1999/xlink"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 service="WPS" version="1.0.0">
        <ows:Identifier>{SERVICE_NAME}</ows:Identifier>
        <wps:DataInputs>
            <wps:Input>
                <ows:Identifier>InputPolygon</ows:Identifier>
                <wps:Data>
                    <wps:ComplexData mimeType="application/json">
                        <![CDATA[{{"type": "Polygon", "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]}}]]>
                    </wps:ComplexData>
                </wps:Data>
            </wps:Input>
            <wps:Input>
                <ows:Identifier>BufferDistance</ows:Identifier>
                <wps:Data>
                    <wps:LiteralData>100</wps:LiteralData>
                </wps:Data>
            </wps:Input>
        </wps:DataInputs>
        <wps:ResponseForm>
            <wps:RawDataOutput mimeType="application/json">
                <ows:Identifier>Result</ows:Identifier>
            </wps:RawDataOutput>
        </wps:ResponseForm>
    </wps:Execute>"""

    headers = {"Content-Type": "text/xml"}
    response = requests.post(URL, data=execute_request, headers=headers)
    
    assert response.status_code == 200, "ExecuteProcess request failed"
    assert '"type": "FeatureCollection"' in response.text, "Invalid ExecuteProcess response"
    print("✅ Test Passed: ExecuteProcess request successful")


# ❌ ERROR TESTS
def test_get_capabilities_missing_service():
    """Test GetCapabilities request with missing service parameter."""
    response = requests.get(f"{URL}?request=GetCapabilities")
    assert response.status_code == 400, "Expected 400 Bad Request for missing service parameter"
    print("❌ Test Passed: GetCapabilities missing service detected")


def test_describe_process_invalid_identifier():
    """Test DescribeProcess request with an invalid process identifier."""
    response = requests.get(f"{URL}?request=DescribeProcess&service=WPS&version=1.0.0&Identifier=InvalidProcess")
    assert response.status_code == 400, "Expected 400 Bad Request for invalid process identifier"
    assert "InvalidProcess" in response.text, "Expected error message for invalid process identifier"
    print("❌ Test Passed: DescribeProcess invalid identifier detected")


def test_execute_process_missing_inputs():
    """Test ExecuteProcess request with missing required inputs."""
    execute_request = f"""<wps:Execute xmlns:wps="http://www.opengis.net/wps/1.0.0"
                 xmlns:ows="http://www.opengis.net/ows/1.1"
                 xmlns:xlink="http://www.w3.org/1999/xlink"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 service="WPS" version="1.0.0">
        <ows:Identifier>{SERVICE_NAME}</ows:Identifier>
        <wps:ResponseForm>
            <wps:RawDataOutput mimeType="application/json">
                <ows:Identifier>Result</ows:Identifier>
            </wps:RawDataOutput>
        </wps:ResponseForm>
    </wps:Execute>"""

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

    print("❌ Test Passed: ExecuteProcess missing inputs detected")


def test_execute_process_invalid_input_format():
    """Test ExecuteProcess request with invalid input format."""
    
    logger.info("Starting test: ExecuteProcess with invalid input format")
    
    execute_request = f"""<wps:Execute xmlns:wps="http://www.opengis.net/wps/1.0.0"
                 xmlns:ows="http://www.opengis.net/ows/1.1"
                 xmlns:xlink="http://www.w3.org/1999/xlink"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 service="WPS" version="1.0.0">
        <ows:Identifier>{SERVICE_NAME}</ows:Identifier>
        <wps:DataInputs>
            <wps:Input>
                <ows:Identifier>InputPolygon</ows:Identifier>
                <wps:Data>
                    <wps:ComplexData mimeType="application/xml">
                        <![CDATA[<InvalidXML>]]>
                    </wps:ComplexData>
                </wps:Data>
            </wps:Input>
            <wps:Input>
                <ows:Identifier>BufferDistance</ows:Identifier>
                <wps:Data>
                    <wps:LiteralData>InvalidNumber</wps:LiteralData>
                </wps:Data>
            </wps:Input>
        </wps:DataInputs>
        <wps:ResponseForm>
            <wps:RawDataOutput mimeType="application/json">
                <ows:Identifier>Result</ows:Identifier>
            </wps:RawDataOutput>
        </wps:ResponseForm>
    </wps:Execute>"""

    headers = {"Content-Type": "text/xml"}

    logger.debug(f"Sending request to: {URL}")
    logger.debug(f"Request Body:\n{execute_request}")

    response = requests.post(URL, data=execute_request, headers=headers)

    logger.debug(f"Received Response Status Code: {response.status_code}")
    logger.debug(f"Received Response Body:\n{response.text}")

    assert response.status_code in [400, 500], f"Expected 400 or 500 but got {response.status_code}"

    root = ET.fromstring(response.text)
    namespace = {"ows": "http://www.opengis.net/ows/1.1"}
    error_message_element = root.find(".//ows:ExceptionText", namespaces=namespace)

    assert error_message_element is not None, "Expected an error message but none found"

    error_message = error_message_element.text

    logger.error(f"Error Message: {error_message}")

    expected_error_keywords = [
        "Invalid input format",
        "parsing error",
        "invalid parameter",
        "unrecognized value",
        "Unable to open datasource"
    ]

    assert any(keyword in error_message for keyword in expected_error_keywords), \
        f"Expected an error message related to invalid input but got: {error_message}"

    logger.success("✅ Test Passed: ExecuteProcess invalid input format detected")


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
