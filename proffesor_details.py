from require_files import connect_driver
from require_files import change_url
from require_files import load_soup as ls
from require_files import load_tag_with_content as load_tag
from urllib.parse import urljoin
import json




# def find_ul(soup):
#      is_ul = True
#      li_s = soup.find_all('li')
     
#      for li in li_s:
#           ul = li.find('ul')
#           anchor = ul.find('a')
#           anchor.text
#           if ul:
#                find_ul(ul)
#           else:
#                is_ul = False
#                break

def extract_data(soup):
    data =[]
    divs = soup.find_all('div',class_="college-content")
    for div in divs:
         sub = div.find('h5',class_="text-white")
         data.append(sub.get_text(strip=True))
    return data

url = "https://www.nagarjunauniversity.ac.in/"
driver = connect_driver.connect_driver()
driver.get(url)
soup = ls.load_soup(driver) 
menu = soup.find('div',class_="main-menu text-right text-lg-center")
topics = []

data = []
required_soup = ""
if menu:
        ul = menu.find('ul')
        if ul:
             lis = ul.find_all('li') 
             required_soup = ul
             for li in lis:
                  new_ul = li.find('ul')
                  if new_ul:
                            new_li_s = new_ul.find_all('li')
                            a = li.find('a')
                            if a:
                                a=a.get_text(strip=True)
                                
                            subtopics = []
                            for new_li in new_li_s:
                                anchor = new_li.find('a')
                                if anchor:
                                    subtopic = anchor.get_text(strip=True)
                                    subtopics.append(subtopic)
                            data.append({a:{"SUB_TOPICS":subtopics}})
                       
                  
                  else:
                       a = li.find('a')
                       if a:
                            a=a.get_text(strip=True)
                       data.append({a:{"SUB_TOPICS":"NO SUB TOPICS"}})

        else:
          print("Error in finding ul")    
else:
    print("Error in loading the Menu bar ")
print(data)
tag_name = load_tag.load_tag(required_soup,"University Colleges")
lis = tag_name.find_all('li')
links = []
data2 = []
for li in lis:
     anchor = li.find('a',href=True)
     link = anchor.find('href')
     if link:
          link=link.strip()
     req_url = urljoin(url,link)
     links.append(req_url)
for link in links:
     soup2=change_url.change_url(req_url)
     dat = extract_data(soup2)

     data2.append(dat)
data3 = data
for item in data3:
    if "Academics" in item:
        item["Academics"]["SUB_TOPICS"] = data2
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(data3, f, indent=4, ensure_ascii=False)

driver.close()

 