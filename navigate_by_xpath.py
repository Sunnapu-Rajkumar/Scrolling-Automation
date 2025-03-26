from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def navigate_by_xpath(driver, xpaths):
    """
    Navigate through the given xpaths sequentially.
    If a single xpath is given, process it normally.
    If multiple xpaths are given, follow them step by step.
    """
    if isinstance(xpaths, str):  # Single XPath case
        xpaths = [xpaths]  # Convert to list for uniform processing

    for xpath in xpaths:
        try:
            element = driver.find_element(By.XPATH, xpath)
            tag_name = element.tag_name.lower()

            if tag_name == "a":  # If it's a link, click it
                element.click()
                time.sleep(2)  # Wait for the page to load
            else:
                print(f"Located element with XPath: {xpath}, but it's not a link.")
        
        except Exception as e:
            print(f"Error locating XPath {xpath}: {e}")

    return driver  # Return updated driver for further actions

# # Example usage
# if __name__ == "__main__":
#     driver = webdriver.Chrome()  # Initialize WebDriver
#     url = "http://www.classics.upenn.edu/"
#     driver.get(url)

#     xpaths = ['//*[@id="block-base-main-menu"]/ul/li[2]/ul/li[1]/a', '//*[@id="another-path"]/div']
#     driver = navigate_by_xpath(driver, xpaths)  # Process XPaths

#     print("Navigation Completed!")
#     driver.quit()
