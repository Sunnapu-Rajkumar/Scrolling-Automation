import require_files.human_sleep as human_sleep

def d_scroll(driver):
    url = driver.current_url
    previous_height = driver.execute_script("return document.body.scrollHeight")
    while True:
         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
         human_sleep.human_sleep()
         current_height = driver.execute_script("return document.body.scrollHeight")
         if previous_height == current_height:
              break
         previous_height = current_height
    return print("Reached page ending")

def scroll_to_bottom(driver):
     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
     return print("Reached page ending")
