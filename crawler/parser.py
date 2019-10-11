import re
from requests_html import HTML, HTMLResponse

def parse_entry_meta(entries):
    r = []
    for entry in entries:
        try:
            r.append(entry.find('div.title > a', first=True).attrs['href'])
        except:
            pass
    return r
    # # every article always have these attributes
    # meta = {
    #     'title': entry.find('div.title', first=True).text,
    #     'vote': entry.find('div.nrec', first=True).text,
    #     'date': entry.find('div.date', first=True).text
    # }
    #
    # if re.compile('已被.*刪除').search(meta['title']):
    #     parse_author = re.search('[\\[\\(](\\w*?)[\\]\\)]', meta['title']) # find the author in parenthesis or bracket
    #     if parse_author:
    #         meta['author'] = parse_author.group(1)
    # else:
    #     meta['author'] = entry.find('div.author', first=True).text
    #     meta['url']: entry.find('div.title > a', first=True).attrs['href']
    #
    # return meta
def get_next_link(r: HTMLResponse):
    html = HTML(html=r.text)
    page_controls = html.find('.action-bar a.btn.wide')
    prev_url = page_controls[1].attrs.get('href') # like '/bbs/Gossiping/index39400.html'
    return get_page_index_from_href(prev_url)

def get_page_index_from_href(url):
    page_idx = re.search(r'index(\d+)', url)
    if page_idx:
        return page_idx.group(1)
    else:
        return
