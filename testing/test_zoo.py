import requests
import xml.etree.ElementTree as ET
from loguru import logger

URL = "http://zookernel/cgi-bin/zoo_loader.cgi"

SERVICE_NAME = "Buffer"

def test_get_capabilities():
    """Test the GetCapabilities request."""
    response = requests.get(f"{URL}?request=GetCapabilities&service=WPS")
    assert response.status_code == 200, "GetCapabilities request failed"
    assert "wps:Capabilities" in response.text, "Invalid GetCapabilities response"
    print("Test Passed: GetCapabilities request successful")

def test_describe_process():
    """Test the DescribeProcess request."""
    response = requests.get(f"{URL}?request=DescribeProcess&service=WPS&version=1.0.0&Identifier={SERVICE_NAME}")
    assert response.status_code == 200, "DescribeProcess request failed"
    assert "wps:ProcessDescriptions" in response.text, "Invalid DescribeProcess response"
    print("Test Passed: DescribeProcess request successful")

def test_execute_process():
    """Test the Execute request using a predefined XML payload and log request/response details."""
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
    
    logger.info("Sending Execute request to WPS service...")
    logger.debug(f"Request XML:\n{execute_request}")

    response = requests.post(URL, data=execute_request, headers=headers)
    
    logger.info(f"Received response with status code: {response.status_code}")
    logger.debug(f"Response content:\n{response.text}")
    
    print("Received Response:", response.text)
    assert response.status_code == 200, "ExecuteProcess request failed"
    assert '"type": "FeatureCollection"' in response.text, "Invalid ExecuteProcess response"

    print("Test Passed: ExecuteProcess request successful")


if __name__ == "__main__":
    test_get_capabilities()
    test_describe_process()
    test_execute_process()
