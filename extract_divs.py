from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def extract_divs_from_page(soup):
    extracted_data = soup.find_all('div' )
    data = [item for item in extracted_data]
    return data