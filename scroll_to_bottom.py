from selenium.webdriver.support.ui import WebDriverWait

def scroll_to_bottom(driver):
    old_position = driver.execute_script("return window.pageYOffset;")
    while True:
        driver.execute_script("window.scroll(0,document.body.scrollHeight)")
        try:
            WebDriverWait(driver, 5).until(
                lambda d: d.execute_script("return window.pageYOffset;") > old_position
            )
        except:
            break  # Break if no new content is loaded
        new_position = driver.execute_script("return window.pageYOffset;")
        if new_position == old_position:
            break   
        old_position = new_position

