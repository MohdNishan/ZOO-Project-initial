## Documentation of Adding a New Test


### 1. Identify the API request type (GET or POST)
Determine whether the new test requires a GET or POST request based on the API's expected input and response structure. Ensure that the correct request method is used to communicate with the API.

### 2. Create a new file in `requests/` for storing XML requests
For tests requiring XML payloads, store the request data in a separate file within the `requests/` directory. This approach keeps the test data organized, reusable, and easy to modify.

### 3. Modify XML dynamically if needed
If the XML request requires customization, use the `modify_xml` function. This function allows dynamic updates to XML elements, making tests flexible and adaptable to different scenarios. Example usage:
```python
replacements = {".//ows:Identifier": "NewProcess", ".//wps:LiteralData": "UpdatedValue"}
modified_xml = modify_xml("requests/execute_template.xml", replacements)
```

### 4. Implement the test function in `test_zoo.py`
Write a structured test function in `test_zoo.py` that sends the request, verifies the response, and includes assertions to check expected results. Example:
```python
def test_new_api_functionality(self):
    response = requests.get(f"{URL}?request=NewRequestType&service=WPS")
    self.assertEqual(response.status_code, 200, "Unexpected status code")
    self.assertIn("ExpectedResponseTag", response.text, "Expected content not found")
    logger.success("✅ Test Passed: New API functionality works correctly")
```

### 5. Log important details
Use `logger.info()` to record key details such as request parameters, response status, and error messages. This enhances traceability and debugging. Example:
```python
logger.info(f"Sending request: {URL}?request=NewRequestType&service=WPS")
logger.debug(f"Response received: {response.text[:500]}")
```

### 6. Run the test and validate the response
Execute the test script using:
```sh
python -m unittest test_zoo.py
```
Analyze the response and confirm that it meets the expected success or failure conditions. If the test fails, refine the logic or update the request parameters.

### 7. Debug using Loguru if needed
If errors occur, leverage Loguru for debugging by capturing response content and failure reasons. Example:
```python
except Exception as e:
    logger.error(f"❌ Test Failed: {e}")
    self.fail(f"Unexpected error: {e}")
```

### 8. Commit successful tests to the repository
Once the test passes, document any necessary changes and commit the updated test files to the repository. Ensure proper version control and integration with the project’s testing framework.

