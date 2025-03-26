def extract_paragraph_from_page(soup):
    # divs = soup.find_all('div' )
    paragraphs = soup.find_all('p')
    data = []
    div = soup.find('div',class_="main-body generic")
    if div:
        paras = div.find_all('p')
        # data.extend(i.get_text() for i in paras)
        for para in paras:
                text = para.get_text(strip=True).replace('\xa0','')
                if text :
                    data.append(text)
    for paragraph in paragraphs:
        text  = paragraph.get_text(strip=True).replace('\xa0','')
        if text and text not in data :
                    data.append(text)
    return data