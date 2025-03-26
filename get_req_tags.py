from bs4 import BeautifulSoup

def parse_attrs(attr_list):
    attrs = {}
    if isinstance(attr_list, str):
        attr_list = [attr_list]
    for item in attr_list:
        if '=' in item:
            key, value = item.split('=', 1)
            if value.lower() == 'true':
                value = True
            attrs[key] = value
    return attrs

# def get_req_tag(data_list, html_content):
#     if isinstance(html_content, (BeautifulSoup, type(BeautifulSoup('<html></html>').find('div')))):
#         node = html_content
#     else:
#         soup = BeautifulSoup(html_content, 'html.parser')
#         node = soup
    
#     for tag in data_list:
#          if isinstance(tag, str):
#             node = node.find(tag) if node else None
#          elif isinstance(tag, dict):
#             for tag_name, attr_list in tag.items():
#                 attrs = parse_attrs(attr_list)
#                 node = node.find(tag_name, **attrs) if node else None
#          else:
#             print("Unsupported data format")
#             continue

#     return node if node else None
                
def get_req_tag(data_list, html_content):
    # Handle None case first
    if html_content is None:
        return None
        
    # Check if content is already a BeautifulSoup element or Tag
    if hasattr(html_content, 'find'):
        # It's already a BeautifulSoup object or Tag
        node = html_content
    else:
        try:
            # Try to parse it as HTML string
            soup = BeautifulSoup(str(html_content), 'html.parser')
            node = soup
        except Exception as e:
            print(f"Error parsing HTML: {e}")
            return None
    
    for tag in data_list:
        if node is None:
            break
            
        if isinstance(tag, str):
            node = node.find(tag)
        elif isinstance(tag, dict):
            for tag_name, attr_list in tag.items():
                attrs = parse_attrs(attr_list)
                node = node.find(tag_name, **attrs)
                break  # Only process the first key-value pair
        else:
            print("Unsupported data format")
            continue

    return node
def gettag_text(data_list, html_content):
    node = get_req_tag(data_list, html_content)
    return node.get_text(strip=True) if node else None

def gettag_link(data_list, html_content):
    node = get_req_tag(data_list, html_content)
    return node.get('href').strip() if node else None
    
     
# Example usage
data = ['html', 'body', {'div':['class_=div_class','id=div']}, 'p', 'span', {'a' :'href=True'}]
html = """
<html>
    <body>
        <div class="div_class" id="div">
            <p>
                <span class='test_match'>
                    <a role="Profressor" href="http://example.com">
                        Hello World
                    </a>
                </span>
            </p>
        </div>
    </body>
</html>
"""

# print(gettag(data, html),"\n")
# print(gettag_text(data, html),"\n")
# print(gettag_link(data, html),"\n")

