from require_files import connect_driver
from require_files import change_url
from require_files import load_soup as ls
from require_files import load_tag_with_content as load_tag
from require_files import extract_links_classname 
from require_files import download_excel as de
from require_files import data_loader
from require_files import get_req_tags
from urllib.parse import urljoin
from urllib.parse import urlparse
import json
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import time

url = "https://www.upenn.edu/"
university = "penn university of pennsylvania"
    
def colleges_list():
            colleges = {}
            driver = connect_driver.connect_driver()
            driver.get(url)
            page_source = ls.load_pagesource(driver)
            # soup = ls.load_soup(driver)
            admissions = driver.find_element(By.XPATH,'//*[@id="primary-navigation"]/ul/li[2]/a')
            colleges_linK = admissions.get_attribute('href').strip()
            colleges_url = urljoin(url,colleges_linK)
            page_source2,_ = change_url.change_url_pagesource(colleges_url)
            soup = BeautifulSoup(page_source2, "html.parser")
            college_link_list = soup.find('ul',class_="quick-links__list")
            college_lis = college_link_list.find_all('li')
            for li in college_lis:
                coll = li.find('a',href=True)
                college_name = coll.text.strip()
                college_url = coll.get('href').strip()
                college_url = college_url.strip()
                colleges[college_name]= college_url
                
            de.download_excel(colleges,"colleges")
            driver.close()

def department_list(): 
            driver = connect_driver.connect_driver()
            driver.get(url)
            page_source = ls.load_pagesource(driver)
            departments ={}
            colleges = data_loader.dynamic_loader("colleges.xlsx",return_type="dict_of_arrays")
            for college_name,college_link in colleges.items(): 
                                         
                next_url = college_link[0]
            page_source3,_ = change_url.change_url_pagesource(url=next_url)
            page_source4,_ = change_url.change_url_xpath(url=next_url,xpath="/html/body/div/div/footer/div/div[3]/address/div[2]/div[1]/p[1]/a[2]")
            soup = BeautifulSoup(page_source4,"html.parser")
            department = extract_links_classname.extract_links(mainurl=url, soup=soup ,class_name="field-p-feat-links-links")
            for department_name, department_link in department.items():
                departments[department_name] = department_link
    
            de.download_excel(departments,"departments_1")

def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ('http', 'https') and parsed.netloc != ''

def depart1XXX():
    departments = data_loader.dynamic_loader("departments_1.xlsx", return_type="dict_of_arrays")
    professor_details = {}

    for depart_name, depart_link in departments.items():
        departurl = depart_link[0] if isinstance(depart_link, list) else depart_link
        departmentname = depart_name
        # Validate URL
        if not is_valid_url(departurl):
            print(f"❌ Skipping invalid URL for {depart_name}: {departurl}")
            continue

        print(f"✅ Scraping {depart_name}: {departurl}")
        driver = connect_driver.connect_driver()
        driver.get(departurl)
        page_source = ls.load_pagesource(driver)
        page_source2, _ = change_url.change_url_xpath(departurl, "/html/body/div[1]/div[2]/section/div/article/div/div[4]/div/div/div[3]/div/div/h3/a")
        soup2 = BeautifulSoup(page_source2, "html.parser")
        req_profs = soup2.find_all('span', class_="field-content")
        professor_details[departmentname] = []

        for req_prof in req_profs:
            details = req_prof.find("summary", class_="col-xs-12")
            if details:
                h3 = details.find('h3')
                if h3:
                    anchor = h3.find('a', href=True)
                    p_name = anchor.get_text(strip=True) if anchor else "PROFESSOR HAS NO NAME"
                else:
                    p_name = "PROFESSOR HAS NO NAME"

                title = details.find('p', class_="title")
                p_affiliation = ""
                if title:
                    spans = title.find_all('span', class_="title")
                    for span in spans:
                        p_affiliation += span.get_text(strip=True)
                else:
                    p_affiliation = "PROFESSOR HAS NO AFFILIATION"

                contact = details.find('p', class_="contact")
                if contact:
                    email = contact.find('span', class_="email")
                    if email:
                        email_details = email.find('a', class_="mailto", href=True)
                        p_email = email_details.get_text(strip=True) if email_details else "NO -- EMAIL"
                    else:
                        p_email = "PROFESSOR HAS NO E-MAIL"
                else:
                    p_email = "PROFESSOR HAS NO E-MAIL"
                
                professor_details[departmentname].append([p_name, p_affiliation, p_email])
            else:
                print(f"⚠️ Error extracting details for department: {depart_name}")

        driver.close()

    # Save once after all departments are processed
    de.download_excel(professor_details, "depart1xxx.xlsx")

def depart1():
        departments = data_loader.dynamic_loader("departments_1.xlsx", return_type="dict_of_arrays")
        professor_details = {}
         
        for depart_name, depart_link in departments.items():
            
            departurl = depart_link[0] if isinstance(depart_link, list) else depart_link
            departmentname = depart_name
        # Validate URL
            if not is_valid_url(departurl):
              print(f"❌ Skipping invalid URL for {depart_name}: {departurl}")
              continue

            departurl = depart_link[0] if isinstance(depart_link, list) else depart_link
            driver = connect_driver.connect_driver()
            driver.get(departurl)
            page_source = ls.load_pagesource(driver)
            page_source2, _ = change_url.change_url_xpath(departurl, "/html/body/div[1]/div[2]/section/div/article/div/div[4]/div/div/div[3]/div/div/h3/a")
            soup2 = BeautifulSoup(page_source2, "html.parser")
            req_profs = soup2.find_all('span', class_="field-content")
            professor_details[depart_name] = []

            for req_prof in req_profs:
                details = req_prof.find("summary", class_="col-xs-12")
                if details:
                    h3 = details.find('h3')
                    if h3:
                        anchor = h3.find('a', href=True)
                        p_name = anchor.get_text(strip=True) if anchor else "PROFESSOR HAS NO NAME"
                    else:
                        p_name = "PROFESSOR HAS NO NAME"

                    title = details.find('p', class_="title")
                    p_affiliation = ""
                    if title:
                        spans = title.find_all('span', class_="title")
                        for span in spans:
                            p_affiliation += span.get_text(strip=True)
                    else:
                        p_affiliation = "PROFESSOR HAS NO AFFILIATION"

                    contact = details.find('p', class_="contact")
                    if contact:
                        email = contact.find('span', class_="email")
                        if email:
                            email_details = email.find('a', class_="mailto", href=True)
                            p_email = email_details.get_text(strip=True) if email_details else "NO -- EMAIL"
                        else:
                            p_email = "PROFESSOR HAS NO E-MAIL"
                    else:
                        p_email = "PROFESSOR HAS NO E-MAIL"
                    
                    professor_details[depart_name].append([p_name, p_affiliation, p_email])
                else:
                    print(f"Error extracting details for department: {depart_name}")

            driver.close()

            de.download_excel(professor_details, "Africana Studies.xlsx")

def depart2():
    # Load departments from local file
    departments = data_loader.dynamic_loader("departments_1.xlsx", return_type="dict_of_arrays")

    professor_details = {}

    for depart_name, depart_link in departments.items():
        departurl = depart_link[1] if isinstance(depart_link, list) else depart_link
        depart_name = depart_name[1]
        if not is_valid_url(departurl):
            print(f"❌ Skipping invalid URL for {depart_name}: {departurl}")
            continue
        soup1 = change_url.change_url(departurl)
        _, driver2 = change_url.change_url_xpath(
            departurl, '/html/body/div[4]/div[6]/div/div/div/div[2]/a'
        )
        current_url = driver2.current_url
        page_source2, _ = change_url.change_url_xpath(
            current_url, "/html/body/div[5]/div/section/div/div/div/div[1]/div/div/div[2]/a"
        )
        departurl = current_url
        soup2 = BeautifulSoup(page_source2, "html.parser")
        req = soup2.find(class_="span9 pull-right")
        professor_details[depart_name] = []

        req_profs = []
        if req:
            ul = req.find('ul', class_='unstyled')
            if ul:
                req_profs = ul.find_all('li')

        for req_prof in req_profs:
            p_name = "N/A"
            p_affilation = "N/A"
            p_email = "N/A"

            details = req_prof.find("h2", class_="field-content")
            if details:
                anchor = details.find("a", href=True)
                if anchor:
                    anchor_href = anchor.get('href')
                    next_url = urljoin(departurl, anchor_href.strip())
                    soup = change_url.change_url(next_url)
                    if soup:
                        name = soup.find('h1', class_="page-header")
                        if name:
                            p_name = name.get_text(strip=True)
                        prof = soup.find(class_="profile-details span6")
                        if prof:
                            detail = prof.find(
                                class_="field field-name-field-official-title field-type-text field-label-hidden"
                            )
                            if detail:
                                p_affilation = detail.get_text(strip=True)
                            email = prof.find('a', class_="mailto", href=True)
                            if email:
                                p_email = email.get_text(strip=True)
                            else:
                                print(f"Email missing for {p_name}")
                        else:
                            print(f"No profile details for {p_name}")
                    else:
                        print("Error loading professor page")
                else:
                    print("No faculty URL found")
            else:
                print("No professor details block found")

            professor_details[depart_name].append([p_name, p_affilation, p_email])

        driver2.close()

    print(professor_details)
    de.download_excel(professor_details, "Anthropology.xlsx")

def depart3():
    # Load departments from local file
    departments = data_loader.dynamic_loader("departments_1.xlsx", return_type="dict_of_arrays")
    professor_details = {}

    for depart_name, depart_link in departments.items():
        departurl = depart_link[2] if isinstance(depart_link, list) else depart_link
        if not is_valid_url(departurl):
            print(f"❌ Skipping invalid URL for {depart_name}: {departurl}")
            continue
        
        departmentname = depart_name
        soup1 = change_url.change_url(departurl)
        page_source, driver = change_url.change_url_xpath(
            departurl, '//*[@id="block-base-main-menu"]/ul/li[2]/ul/li[1]/a'
        )
        soup2 = BeautifulSoup(page_source, "html.parser")
        reqs = soup2.findAll('summary', class_="col-md-8")
        professor_details[departmentname] = []
        
        for req in reqs:
            p_name = "N/A"
            p_affilation = "N/A"
            p_email = "N/A"
            
            # For name - we need to find the last <a> in <h3> with text
            h3_elem = get_req_tags.get_req_tag(['h3'], req)
            if h3_elem:
                a_elements = h3_elem.find_all('a')
                for a in a_elements:
                    if a.get_text(strip=True):
                        p_name = a.get_text(strip=True)
                        break
            
            # For affiliation
            p_affilation = get_req_tags.gettag_text([{'p':'class_=title'}, {'span':'class_=title'}], req) or "N/A"
            
            # For email
            p_email = get_req_tags.gettag_text([{'p':'class_=contact'}, 'a'], req) or "N/A"
            
            professor_details[departmentname].append([p_name, p_affilation, p_email])
        
        driver.close()

    print(professor_details)
    de.download_excel(professor_details, "Biology.xlsx")

def depart4():
    # Load departments from local file
    departments = data_loader.dynamic_loader("departments_1.xlsx", return_type="dict_of_arrays")
    professor_details = {}

    for depart_name, depart_link in departments.items():
        departurl = depart_link[3] if isinstance(depart_link, list) else depart_link
        if not is_valid_url(departurl):
            print(f"❌ Skipping invalid URL for {depart_name}: {departurl}")
            continue
        
        departmentname = depart_name
        soup1 = change_url.change_url(departurl)
        page_source, driver = change_url.change_url_xpath(
            departurl, '//*[@id="block-base-main-menu"]/ul/li[2]/a'
        )
        current_url = driver.current_url
        page_source2,_ = change_url.change_url_xpath(current_url,'//*[@id="block-mainnavigation"]/div/div/div/div/div[1]/div[1]/a')
        soup2 = BeautifulSoup(page_source2, "html.parser")
        reqs = soup2.findAll('summary', class_="col-md-9")
        professor_details[departmentname] = []
        
        for req in reqs:
            p_name = "N/A"
            p_affilation = "N/A"
            p_email = "N/A"
            
            # For name - we need to find the last <a> in <h3> with text
            h3_elem = get_req_tags.get_req_tag(['h3'], req)
            if h3_elem:
                a_elements = h3_elem.find_all('a')
                for a in a_elements:
                    if a.get_text(strip=True):
                        p_name = a.get_text(strip=True)
                        break
            
            # For affiliation
            p_affilation = get_req_tags.gettag_text([{'p':'class_=title'}, {'span':'class_=title'}], req) or "N/A"
            
            # For email
            p_email = get_req_tags.gettag_text([{'p':'class_=contact'}, 'a'], req) or "N/A"
            
            professor_details[departmentname].append([p_name, p_affilation, p_email])
        
        driver.close()

    print(professor_details)
    de.download_excel(professor_details, "Chemistry.xlsx")

def depart5():
    # Load departments from local file
    departments = data_loader.dynamic_loader("departments_1.xlsx", return_type="dict_of_arrays")
    professor_details = {}

    for depart_name, depart_link in departments.items():
        departurl = depart_link[4] if isinstance(depart_link, list) else depart_link
        if not is_valid_url(departurl):
            print(f"❌ Skipping invalid URL for {depart_name}: {departurl}")
            continue
        
        departmentname = depart_name
        soup1 = change_url.change_url(departurl)
        page_source, driver = change_url.change_url_xpath(
            departurl, '//*[@id="block-base-main-menu"]/ul/li[2]/ul/li[2]/a')
        current_url = driver.current_url
        print(current_url)
        
        soup2 = BeautifulSoup(page_source, "html.parser")
        reqs = extract_links_classname.extract_links(current_url,soup2,"website",False,departurl)
        # print(departurl)
        # print(reqs)
        
        professor_details[departmentname] = []
        # print("Created Professor details in Dict")
        for req in reqs.values():
            print("Started Loop")
            p_name = "N/A"
            p_affilation = "N/A"
            p_email = "N/A"
            soup = change_url.change_url(req)
            # For name  
            p_name = get_req_tags.gettag_text([{'h1':'class_=page-header'},'span'],soup) or "N/A"
            # For affiliation
            p_affilation = get_req_tags.gettag_text([{'p':'class_=title'},'span'], soup) or "N/A"
            
            # For email
            p_email = get_req_tags.gettag_text([{'p':'class_=contact'}, {'span':'class_=email'},{'a':'class_=mailto'}], soup) or "N/A"
            
            professor_details[departmentname].append([p_name, p_affilation, p_email])
        
        driver.close()

    print(professor_details)
    de.download_excel(professor_details, "Cinema and Media Studies.xlsx")

def depart6():
    # Load departments from local file
    departments = data_loader.dynamic_loader("departments_1.xlsx", return_type="dict_of_arrays")
    professor_details = {}

    for depart_name, depart_link in departments.items():
        departurl = depart_link[5] if isinstance(depart_link, list) else depart_link
        if not is_valid_url(departurl):
            print(f"❌ Skipping invalid URL for {depart_name}: {departurl}")
            continue
        
        departmentname = depart_name
        soup1 = change_url.change_url(departurl)
        page_source, driver = change_url.change_url_xpath(
            departurl, '//*[@id="block-base-main-menu"]/ul/li[2]/ul/li[2]/a')
        current_url = driver.current_url
        print(current_url)
        
        soup2 = BeautifulSoup(page_source, "html.parser")
        reqs = extract_links_classname.extract_links(current_url,soup2,"website",False,departurl)
        # print(departurl)
        # print(reqs)
        
        professor_details[departmentname] = []
        # print("Created Professor details in Dict")
        for req in reqs.values():
            print("Started Loop")
            p_name = "N/A"
            p_affilation = "N/A"
            p_email = "N/A"
            soup = change_url.change_url(req)
            # For name  
            p_name = get_req_tags.gettag_text([{'h1':'class_=page-header'},'span'],soup) or "N/A"
            # For affiliation
            p_affilation = get_req_tags.gettag_text([{'p':'class_=title'},'span'], soup) or "N/A"
            
            # For email
            p_email = get_req_tags.gettag_text([{'p':'class_=contact'}, {'span':'class_=email'},{'a':'class_=mailto'}], soup) or "N/A"
            
            professor_details[departmentname].append([p_name, p_affilation, p_email])
        
        driver.close()

    print(professor_details)
    de.download_excel(professor_details, "Classical Studies.xlsx")
def main():  
            # colleges_list()    
            # department_list()   
            depart1()
            # depart1XXX()
            
            depart2()
            depart3()
            depart4()
            depart5()
            depart6()
            
if __name__ == "__main__":
     main()

      
