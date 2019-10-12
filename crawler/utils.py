import re

def make_ptt_url(domain, board, page=""):
    return f'{domain}/bbs/{board}/index{page}.html'

def get_cat_from_title(title):
    find_cat = re.search('\\[(\\w*?)\\]', title)
    if find_cat:
        category = find_cat.group(1)
    else:
        category = "unknown"
    return category

def get_user_handle(s):
    if not s:
        return ""
    return s.split(" ")[0]

def parse_ip(text):
    match = re.search(r'(\d+\.\d+\.\d+\.\d+)(.*)', text)
    if match:
        ip = match.group(1)
        rest = match.group(2)
    else:
        ip = 'unknown'
        rest = text
    return ip, rest.strip("() ")

def flatten(nested):
    for sublist in nested:
        for element in sublist:
            yield element

def get_page_index_from_href(url):
    page_idx = re.search(r'index(\d+)', url)
    if page_idx:
        return page_idx.group(1)
