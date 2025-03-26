def load_tag(soup,text):
    target_tag_name = ""
    target_tag = soup.find(lambda tag: tag.name and text in tag.text)
    if target_tag:
        print("Found ",target_tag.name)
        print("Text content",target_tag.text)
        # tag_name = target_tag.name
        target_tag_name = target_tag
    else:
        print("NO mathing tag found")
        target_tag_name = None
    return target_tag_name
