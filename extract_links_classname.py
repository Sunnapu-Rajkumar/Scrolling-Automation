from urllib.parse import urljoin

def extract_links(url, soup, class_name, find_all_links=bool, mainurl=None):
    links = {}
    count = 1  # Counter for unique numbering
    if find_all_links :
        anchors = soup.find_all('a', class_=class_name, href=True)  
        for anchor in anchors:
                if not anchor:
                    continue
                title_text = anchor.get_text(strip=True) or "Title"  # Ensure title isn't empty
                title = f"{title_text} {count}"  # Append counter for uniqueness
                link = anchor.get('href') 
                if link:
                    link = link.strip()
                else:
                    link = "No link"
                full_link = urljoin(mainurl if mainurl else url, link)

                links[title] = full_link
                count += 1  # Increment counter for uniqueness

        return links
    else :
        elements = soup.find_all(class_=class_name)
        for element in elements:
            anchor = element.find('a', href=True)
            if not anchor:
                continue
            title_text = anchor.get_text(strip=True) or "Title"  # Ensure title isn't empty
            title = f"{title_text} {count}"  # Append counter for uniqueness
            link = anchor.get('href') 
            if link:
                link = link.strip()
            else:
                link = "No link"
            full_link = urljoin(mainurl if mainurl else url, link)

            links[title] = full_link
            count += 1  # Increment counter for uniqueness

    return links

    

    
        