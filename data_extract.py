from selenium.webdriver.common.by import By
from require_files import connect_driver
from require_files import load_soup
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
            tag = ""
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
    data_extract = structure
    if not isinstance(data_extract, dict) or len(data_extract) != 1:
        print("Structure must be a dictionary with exactly one key-value pair")
        return {}
    
    return helpingmethod(driver, structure)

def main():
    driver = connect_driver.connect_driver()
    url = "https://www.classics.upenn.edu/people"
    driver.get(url)
    data_extract = {("class_name","col-md-8") :
                    [
                        ("")
                    ]
                   }
    extract_data(driver, data_extract)
main()