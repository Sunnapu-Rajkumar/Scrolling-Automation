from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def click_next_button(driver):
    try:
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']"))  # Update XPath if needed
        )
        print("Clicking 'Next' button...")
        next_button.click()
        time.sleep(3)  # Wait for new content to load after clicking
        return True  # Successfully clicked "Next"
    except:
        print("No 'Next' button found. Exiting...")
        return False  # No "Next" button found, exit loop
    