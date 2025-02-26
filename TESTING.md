

## Documentation of Adding a New Test

1. Identify the API request type (GET or POST): 
      Determine whether the new test requires a GET or POST request based on the API's expected input and response structure.

2. Create a new file in requests/ for extracting the XML contents: 
      Store the XML request payload in a separate file within the requests/ directory to maintain organized and reusable test data.

3. If modifications are needed, use the modify_xml script (Search and Replace):
      Utilize the modify_xml function to dynamically update specific XML elements before sending the request, ensuring flexibility for different test scenarios.

4. Write a new test function in test_zoo.py: 
      Implement a structured test function in test_zoo.py that sends the request, verifies the response, and includes assertions to confirm expected results.

5. Log important details using logger.info(): 
      Use logger.info() to record key information, such as request parameters, response status, and error messages, for better traceability and debugging.

6. Run the test and validate the response: 
      Execute the test script, analyze the response, and confirm that it meets the expected success or failure conditions.

7. While facing any issue or encountering an error, use Loguru for debugging: 
      Leverage loguru for detailed logging and debugging, capturing response content and failure reasons to troubleshoot test failures effectively.

8. If the test is successful, commit it to the repository: 
      Once the test passes all validations, document any necessary changes and commit the updated test files to the repository for future reference and integration.







