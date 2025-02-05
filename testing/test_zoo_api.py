import requests

BASE_URL = "http://localhost:8080/cgi-bin/zoo_loader.cgi?request=GetCapabilities&service=WPS"

def test_service_status():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    print("Test Passed: ZOO-Project is running")

if __name__ == "__main__":
    test_service_status()
