# from driver_scrap_filles import data_extract
# from driver_scrap_filles import navigate_by_xpath
from driver_scrap_filles import navigate_data_extract

 
url = "http://www.classics.upenn.edu/"
xpath = '//*[@id="block-base-main-menu"]/ul/li[2]/ul/li[1]/a'  # Example XPath

data_extract = {
        ("class_name","col-md-8"):
        [
            ("tag_name","h3"),
            {
                ("class_name","title"):"span"
            },
            {
                   ("class_name", "contact"):
                   { ("class_name", "span"):["email"]}
            }
        ]  
              }

extracted_data =  navigate_data_extract.data_scrap(url, xpath, data_extract)
print(extracted_data)

