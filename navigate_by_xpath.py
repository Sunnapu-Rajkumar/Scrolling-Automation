from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from required_files import human_sleep
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def navigate_by_xpath(driver, xpaths,changeurl=True,url=None):
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
            if changeurl:
                if tag_name == "a":  # If it's a link, click it
                    element.click() 
                    print(f"Clicked link: {xpath}")
                    human_sleep.human_sleep()
                else:
                    print(f"Located element with XPath: {xpath}, but it's not a link. Trying href...")

                    href = element.get_attribute('href')
                    if href:
                        new_url = urljoin(url if url else driver.current_url, href)
                        driver.get(new_url)
                        page_source =driver.page_source
                        print(f"Navigated to {new_url} using href.")
                        time.sleep(3)
                    else:
                        print(f"No href found for {xpath}. Skipping...")
            else :
                print("Extracting the element with x_path")
        except Exception as e:
            print(f"Error navigating with XPath {xpath}: {e}")
    soup =BeautifulSoup(driver.page_source,"html.parser")
    return driver,soup # Return updated driver for further actions

# # Example usage
# if __name__ == "__main__":
#     driver = webdriver.Chrome()  # Initialize WebDriver
#     url = "http://www.classics.upenn.edu/"
#     driver.get(url)

#     xpaths = ['//*[@id="block-base-main-menu"]/ul/li[2]/ul/li[1]/a', '//*[@id="another-path"]/div']
#     driver = navigate_by_xpath(driver, xpaths)  # Process XPaths

#     print("Navigation Completed!")
#     driver.quit()