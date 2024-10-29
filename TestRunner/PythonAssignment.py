import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pathlib import Path


def load_json_data(file_path):
    """Load JSON data from the specified file path."""
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            print(data)  # Print the loaded data for verification
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        exit(1)
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        exit(1)


def setup_driver():
    """Set up the Chrome WebDriver."""
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(30)  # Set implicit wait
    return driver


def input_json_data(driver, json_data):
    """Input JSON data into the textarea and refresh the table."""
    try:
        text_area = driver.find_element(By.XPATH, "//textarea[@id='jsondata']")
        text_area.clear()  # Clear the text area if necessary
        text_area.send_keys(json_data)  # Input the JSON data
        driver.find_element(By.ID, "refreshtable").click()  # Refresh the table
        time.sleep(5)  # Wait to observe the result (optional)
    except Exception as e:
        print("Error interacting with the text area or clicking the refresh button:", e)


def assert_table_data(driver, expected_values):
    """Assert that the table data matches the expected values from JSON."""
    elements = driver.find_elements(By.XPATH, '//table[@id="dynamictable"]//tr/td')
    actual_values = [element.text.strip() for element in elements]  # Get and strip text from elements

    # Check if the number of cells matches the number of expected values
    assert len(actual_values) == len(expected_values), "Mismatch in number of table cells and JSON values"

    # Loop through each element and assert its text matches the expected JSON value
    for i, (actual_text, expected_text) in enumerate(zip(actual_values, expected_values)):
        assert actual_text == expected_text, f"Mismatch at index {i}: Expected '{expected_text}', but got '{actual_text}'"
        print(f"Matched value: {actual_text}")  # Optional: Print matching values


def main():
    # Step 1: Define the relative path to the JSON file
    json_file_path = Path('..') / 'TestData' / 'testdata.json'

    # Step 2: Load the JSON data
    data = load_json_data(json_file_path)

    # Step 3: Set up the WebDriver
    driver = setup_driver()

    # Step 4: Open the specified URL
    driver.get("https://testpages.herokuapp.com/styled/tag/dynamic-table.html")

    # Step 5: Click on the summary element to expand (if necessary)
    try:
        driver.find_element(By.TAG_NAME, "summary").click()
        time.sleep(5)  # Wait for the content to load
    except Exception as e:
        print("Error clicking on the summary:", e)

    # Step 6: Prepare to input JSON data into the text area
    json_data = json.dumps(data)  # Convert Python object back to JSON string
    input_json_data(driver, json_data)

    # Step 7: Prepare expected values from JSON data for assertions
    expected_values = [str(value) for person in data for value in person.values()]

    # Step 8: Assert the table data
    assert_table_data(driver, expected_values)

    # Step 9: Close the browser after completion
    driver.quit()  # Close the browser and end the WebDriver session


if __name__ == "__main__":
    main()