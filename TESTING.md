## Writing Tests

1. ## Create a new test function
   - Use `requests` to test any API endpoints. Example:
     ```python
     def test_new_endpoint():
         response = requests.get('http://localhost/api/new-endpoint')
         assert response.status_code == 200
     ```

2. ## Integrate the test
   - Add your new test function to the `test_zoo_api.py` file or any new test module.
   
3. ## Run tests
   - Use the `docker run` command or simply run the Python script:
     ```bash
     python test_zoo_api.py
     ```
