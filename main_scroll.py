from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager 
from urllib.parse import urljoin
import pandas as pd
import connect_driver
import page_soup
import scroll_to_bottom

driver = connect_driver.connect_driver()
url = "https://www.amazon.in/s?i=electronics&rh=n%3A1389432031&s=popularity-rank&fs=true&ref=lp_1389432031_sar"

try:
    soup = page_soup.page_soup(driver)
    scroll_to_bottom.scroll_to_bottom(driver)
    

finally:
    driver.quit()
