from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
from require_files import connect_driver
from require_files import human_sleep
from urllib.parse import urljoin

def navigate_by_xpath(driver, xpaths):
    """
    Navigate through the given XPaths sequentially.
    - If a single XPath is given, process it normally.
    - If multiple XPaths are given, follow them step by step.
    """
    if isinstance(xpaths, str):  # Convert single XPath to list
        xpaths = [xpaths]

    for xpath in xpaths:
        try:
            element = driver.find_element(By.XPATH, xpath)
            driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(1)

            tag_name = element.tag_name.lower()
            if tag_name == "a":  # If it's a link, click it
                element.click()
                print(f"Clicked link: {xpath}")
                human_sleep.human_sleep()
            else:
                print(f"Located element with XPath: {xpath}, but it's not a link. Trying href...")

                href = element.get_attribute('href')
                if href:
                    new_url = urljoin(driver.current_url, href)
                    driver.get(new_url)
                    print(f"Navigated to {new_url} using href.")
                    time.sleep(3)
                else:
                    print(f"No href found for {xpath}. Skipping...")
        except Exception as e:
            print(f"Error navigating with XPath {xpath}: {e}")

    return driver  # Return updated driver for further actions
from selenium.webdriver.common.by import By

def helpingmethod(driver, data=None):
    extract_data = []
    if data is None:
        return None

    for index, value in data.items():  # Iterate correctly through dict
        if isinstance(index, tuple) and len(index) == 2:
            first_element = index[0].upper() 
            second_element = index[1]

            if hasattr(By, first_element):  
                try:
                    tag = driver.find_element(getattr(By, first_element), second_element)
                    if not tag:
                        print(f"No such Tag found: {second_element}")
                except Exception as e:
                    print(f"Error finding element: {e}")
            else:
                print(f"'{first_element}' is NOT a valid attribute of By.")

        else:
            print("Key should be a tuple with exactly 2 elements")

        # Process value (List of tags or nested dicts)
        if isinstance(value, list):
            for i in value:
                if isinstance(i, str):  # If it's a tag name
                    try:
                        tag = driver.find_element(By.TAG_NAME, i)
                        extract_data.append(tag.text)
                    except Exception as e:
                        print(f"Error finding tag {i}: {e}")

                elif isinstance(i, dict):  # If it's a nested structure
                    helpingmethod(driver, i)
                else:
                    print("Invalid Data Entry in List")

    return extract_data 

def extract_data(driver, structure):
    if not isinstance(structure, dict) or len(structure) != 1:
        print("Structure must be a dictionary with exactly one key-value pair")
        return {}

    return helpingmethod(driver, structure)



def clean_data(data):
    """
    Remove empty values and duplicates from extracted data.
    """
    cleaned_data = {}

    for key, values in data.items():
        if isinstance(values, list):
            non_empty_values = [v for v in values if v.strip()]  # Remove empty strings
            unique_values = list(dict.fromkeys(non_empty_values))  # Remove duplicates
            cleaned_data[key] = unique_values
        else:
            cleaned_data[key] = values

    return cleaned_data

def save_to_excel(data, file_name="extracted_data.xlsx"):
    """
    Save cleaned extracted data into an Excel file.
    """
    cleaned_data = clean_data(data)

    # Ensure all lists are of the same length
    max_length = max(len(v) for v in cleaned_data.values()) if cleaned_data else 0

    # Pad shorter lists with None
    for key in cleaned_data:
        while len(cleaned_data[key]) < max_length:
            cleaned_data[key].append(None)

    df = pd.DataFrame(cleaned_data)
    df.to_excel(file_name, index=False)
    print(f"Data saved to {file_name}")

def data_scrap(url, xpaths=None, data_extract={}):
    """
    Navigate to URL and extract data. If XPath(s) are provided, navigate through them first.
    """
    driver = connect_driver.connect_driver()
    driver.get(url)
    time.sleep(3)  # Allow page to load

    # If XPaths are provided, navigate through them
    if xpaths:
        driver = navigate_by_xpath(driver, xpaths)

    # Extract data from the final page
    extracted_data = extract_data(driver, data_extract)
    # save_to_excel(extracted_data)

    driver.quit()
    return extracted_data

# # Example Usage
# if __name__ == "__main__":
#     url = "http://www.classics.upenn.edu/"
#     xpaths = [
#         '//*[@id="block-base-main-menu"]/ul/li[2]/ul/li[1]/a',  
#         '//*[@id="some-other-path"]'
#     ]  # Example multiple XPaths

#     data_extract = {
#         "class_name": "col-md-8",  
#         "tag_name": "p",  
#         "id": "main-content",  
#         "xpath": "//*[@id='some-element']",  
#     }

#     extracted_data = data_scrap(url, xpaths, data_extract)
#     print(extracted_data)
