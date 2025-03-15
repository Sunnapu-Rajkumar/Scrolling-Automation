from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager 
from urllib.parse import urljoin
import json
import pandas as pd
import connect_driver

def page_soup(driver):
        url = driver.current_url
        driver.get(url)
        WebDriverWait(driver,10).until(ec.presence_of_element_located((By.TAG_NAME,'body')))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source,"html.parser")
        return soup
