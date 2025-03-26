import require_files.connect_driver as cd
from require_files import load_soup as ls
from selenium.webdriver.common.by import By
from urllib.parse import urljoin

def change_url_pagesource(url):
    # driver.close()
    new_driver = cd.connect_driver()
    new_driver.get(url)
    page_source = ls.load_pagesource(new_driver)
    print(f"Pag navigated to {url}")
    return page_source,new_driver


def change_url(url):
    # driver.close()
    new_driver = cd.connect_driver()
    new_driver.get(url)
    soup = ls.load_soup(new_driver)
    print(f"Pag navigated to {url}")
    return soup

def change_url_xpath(url,xpath):
       next_url = ""
       new_driver = cd.connect_driver()
       new_driver.get(url)
       page_source = ls.load_pagesource(new_driver)
       anchor = new_driver.find_element(By.XPATH,xpath)
    #    tag = anchor.find_element('a',href=True)
       if anchor:
            link =anchor.get_attribute('href').strip()
            next_url = urljoin(url,link)
            new_page_source,new_driver = change_url_pagesource(next_url)
            return new_page_source,new_driver
       else:
            print("NO ANCHOR FOUND FOUND")
            return None,new_driver
       
      