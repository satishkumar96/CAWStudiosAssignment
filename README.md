# Dynamic Table JSON Data Automation

This repository contains a Robot Framework test suite designed to automate the process of loading JSON data into a dynamic table on a webpage, verifying that data, and handling other Selenium-based interactions.

## Overview

The test suite performs the following actions:
1. Loads data from a JSON file.
2. Launches a web browser and navigates to a sample dynamic table webpage.
3. Inputs JSON data into a text area and refreshes the table.
4. Verifies that table data matches the expected values from the JSON file.

## Requirements

The test suite is built using **Robot Framework** and **SeleniumLibrary**, with additional support for JSON handling.

### Key Libraries Used:
- **SeleniumLibrary**: Provides browser automation.
- **JSONLibrary**: Allows loading and working with JSON data.
- **BuiltIn, OperatingSystem, Collections, and String**: Core Robot Framework libraries for handling various operations.

## Setup Instructions

### 1. Install Dependencies

Ensure you have Python installed, then install the necessary libraries. Run the following commands in your project directory:

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt` file, you can install the libraries manually:

```bash
pip install robotframework
pip install robotframework-seleniumlibrary
pip install robotframework-jsonlibrary
```

### 2. Run the Tests

To execute the test, simply run:

```bash
robot path/to/your_test_suite.robot
```

### 3. Chromedriver Configuration

There is **no need to manually download and install the Chromedriver** executable file, as the latest versions of Robot Framework automatically manage the driver installation. This simplifies setup and ensures that you always have a compatible driver version for Chrome.

## Project Structure

- **tests/**: Contains the `.robot` files for testing.
- **TestData/**: Stores the `testdata.json` file with sample data to load into the table.
- **requirements.txt**: Lists all dependencies.

## JSON Data Structure

The `testdata.json` file should be structured as follows:

```json
[
    {
        "key1": "value1",
        "key2": "value2",
        ...
    },
    {
        "key1": "value3",
        "key2": "value4",
        ...
    }
]
```

Each JSON object represents a row in the dynamic table, where keys are field names, and values are data to be verified against the table.

## Custom Keywords

The test suite defines custom keywords for actions like loading JSON data, setting up the driver, interacting with the web elements, and verifying table data.

## Example Usage

```robot
*** Settings ***
Library    SeleniumLibrary
Library    JSONLibrary
...

*** Test Cases ***
Test JSON Data In Dynamic Table
    [Documentation]    Loads JSON data, inputs it into a dynamic table, and verifies table contents.
    ${data}    Load JSON Data    ${JSON_FILE_PATH}
    Setup Driver
    Open URL and Expand Summary
    ${json_data}    Evaluate    json.dumps(${data})    json
    Input JSON Data    ${json_data}
    Assert Table Data    ${expected_values}
    Close Browser
```
