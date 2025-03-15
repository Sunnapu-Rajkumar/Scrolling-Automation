from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager 


def connect_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--incognito")
    options.add_argument("--disable-notifications")
    prefs = {
        "profile.default_content_setting_values":{
            "images":2,
            "plugins":2,
            "geolocation":2,
            "notifications":2
        }
    }
    options.add_experimental_option("prefs",prefs)

    driver =webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    print("Driver Installed Sucessfully")
    return driver
