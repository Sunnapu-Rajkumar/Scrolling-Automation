from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException



def load_soup(driver):
    page_source = load_pagesource(driver)
    soup = BeautifulSoup(page_source, "html.parser")
    print("Soup Extracted Sucessfully")
    return soup
def load_pagesource(driver):
     url = driver.current_url
     driver.get(url)
     try :
         WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, 'body')))
     except TimeoutException:
         print("Timeout waiting for the products container.")
     page_source = driver.page_source

     print("Page Source Extracted Sucessfully")
     return page_source

def load_soup_xpath(page_source,xpath):
     req = page_source.find_Element(By.XPATH,xpath)
     return req