from required_files import connect_driver
import pandas as pd
from required_files import navigate_by_xpath
from required_files import extract_data
from required_files import save_data
from required_files import load_excel
from required_files import change_url
url ="https://www.upenn.edu/"
university = "Penn University Of Pennsylvania"
Colleges = []
Departments = []
driver = connect_driver.connect_driver()
driver.get(url)
def getColleges():
    x_path =['//*[@id="primary-navigation"]/ul/li[2]/a']
    driver2,soup=navigate_by_xpath.navigate_by_xpath(driver,x_path,url)
    structure = {
    ("class_name", "quick-links__item", "all"): [  # Select each <li> item
        ("tag_name", "a", "one"),   # Extract <a> text
        ("attribute", "href", "one")  # Extract <a> href attribute
    ]
}
    driver2.close
    data = extract_data.extract_data(driver,structure)
    print(data)
        # Extract college names and links
    colleges_with_links = [{"College Name": item["a"], "URL": item["href"]} for item in data["quick-links__item"] if "a" in item and "href" in item]
    # Extract only college names and append to the Colleges list
    Colleges.extend([item["College Name"] for item in colleges_with_links])
    output_folder = r"C:\Users\rajku\Desktop\Penn_University\Colleges"
    save_data.save_data(Colleges,output_folder)
    # Convert to DataFrame
    df = pd.DataFrame(colleges_with_links)
    save_data.save_excel(df,output_folder)
def departments():
    filepath = r"C:\Users\rajku\Desktop\Penn_University\Colleges.xlsx"
    college_data = load_excel.load_excel(filepath)
    print (college_data)
    for college in college_data:
        url = college.get("URL")
        driver2,soup = change_url.change_url(url)
        
    
def main():
    # getColleges()
    departments()

if __name__ == "__main__":
    main()
def last():
    structure = {
    ("class_name", "col-md-8", "all"): [  # Extract all summary sections
        {
            ("tag_name", "h3", "one"): [  # Extract Name inside <h3>
                ("tag_name", "a", "one")  # Extract the <a> text (Name)
            ]
        },
        {
            ("tag_name", "p", "all"): []  # Extract all <p> (Titles)
        },
        {
            ("class_name", "contact email", "one"): [  # Extract email inside contact section
                ("tag_name", "p", "one")  # Extract email inside <p>
            ]
        }
    ]
}

    # Call your function
    data = extract_data(driver, structure)

    # Process extracted data
    summary_list = []
    for summary in data.get("col-md-8", []):
        name = summary.get("h3", {}).get("a", "Not Found")
        titles = " | ".join([p for p in summary.get("p", []) if p])  # Join multiple <p> as title
        email = summary.get("contact email", {}).get("p", "Not Found")

        summary_list.append({"Name": name, "Title": titles, "Email": email})

    # Print or save the extracted data
    for entry in summary_list:
        print(entry)


    



 
