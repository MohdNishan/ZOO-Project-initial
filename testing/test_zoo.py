import requests

URL = "http://localhost/cgi-bin/zoo_loader.cgi?service=WPS&request=GetCapabilities"

def test_zoo_loader():
    response = requests.get(URL)
    assert response.status_code == 200, "ZOO Project is not responding"
    print("Test Passed: ZOO-Project is running")

if __name__ == "__main__":
    test_zoo_loader()
