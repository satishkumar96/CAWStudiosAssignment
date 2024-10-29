*** Settings ***
Library    SeleniumLibrary
Library    Collections
Library    OperatingSystem
Library    JSONLibrary
Library    BuiltIn
Library    String

*** Variables ***
${URL}                 https://testpages.herokuapp.com/styled/tag/dynamic-table.html
${JSON_FILE_PATH}      ./TestData/testdata.json
${BROWSER}             Chrome
${IMPLICIT_WAIT}       30s
${TEXT_AREA_XPATH}     //textarea[@id='jsondata']
${REFRESH_BUTTON_ID}   refreshtable
${DYNAMIC_TABLE_XPATH}  //table[@id="dynamictable"]//tr/td

*** Keywords ***
Load JSON Data
    [Arguments]    ${file_path}
    ${data}    Load JSON From File    ${file_path}
    Log    ${data}    # Log data for verification
    [Return]    ${data}

Setup Driver
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Implicit Wait    ${IMPLICIT_WAIT}

Input JSON Data
    [Arguments]    ${json_data}
    Clear Element Text    xpath=${TEXT_AREA_XPATH}
    Input Text    xpath=${TEXT_AREA_XPATH}    ${json_data}
    Click Button    id=${REFRESH_BUTTON_ID}
    Sleep    5s  # Optional: Wait to observe the result

Assert Table Data
    [Arguments]    ${expected_values}
    ${elements}    Get WebElements    xpath=${DYNAMIC_TABLE_XPATH}
    ${actual_values}    Create List
    FOR    ${element}    IN    @{elements}
        ${text}    Get Text    ${element}
        ${text}    Strip String    ${text}
        Append To List    ${actual_values}    ${text}
    END

    # Check if the number of cells matches
    Length Should Be    ${actual_values}    ${expected_values.__len__()}

    # Loop through each element and assert its text matches
    FOR    ${i}    IN RANGE    ${expected_values.__len__()}
        Should Be Equal As Strings    ${actual_values[${i}]}    ${expected_values[${i}]}
        Log    Matched value: ${actual_values[${i}]}  # Optional
    END

Open URL and Expand Summary
    Click Element    tag=summary
    Sleep    5s  # Wait for the content to load

*** Test Cases ***
Test JSON Data In Dynamic Table
    # Step 1: Load JSON data
    ${data}    Load JSON Data    ${JSON_FILE_PATH}

    # Step 2: Set up WebDriver and open the specified URL
    Setup Driver

    # Step 3: Expand summary section (if needed)
    Open URL and Expand Summary

    # Step 4: Convert Python object back to JSON string using Evaluate
    ${json_data}    Evaluate    json.dumps(${data})    json

    # Step 5: Input JSON data and refresh the table
    Input JSON Data    ${json_data}

    # Step 6: Prepare expected values from JSON data for assertions
    ${expected_values}    Create List
    FOR    ${person}    IN    @{data}
        FOR    ${value}    IN    @{person.values()}
            Append To List    ${expected_values}    ${value}
        END
    END

    # Step 7: Assert the table data
    Assert Table Data    ${expected_values}

    # Step 8: Close the browser after completion
    Close Browser
