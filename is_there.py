def is_there_text(element):
    req_text = ""
    if element:
        req_text = req_text.get_text(strip=True)
    else:
         print("NO ELEMENT")
         req_text = None
    return req_text

def is_there(element):
    req_text = False
    if element:
         req_text = True
    else:
         print("NO ELEMENT")   
    return req_text