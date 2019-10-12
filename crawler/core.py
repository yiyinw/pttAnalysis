# -*- coding: utf-8 -*-

from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
from requests_html import HTML, HTMLSession, HTMLResponse
import utils
from users import Author, Commentor
from urllib.parse import urljoin
import time

domain = "https://www.ptt.cc/"

class Agent():
    def __init__(self):
        self.session = self._create_session()

    def _create_session(self):
        session = HTMLSession(mock_browser=True)
        session.cookies.set('over18', '1') # log the age
        return session

    def get(self, url):
        response = self.session.get(url)
        return response

agent = Agent()

class Board():
    def __init__(self, name):
        self.name = name
        self._cur_page = None

    def get_post_list(self, num_posts):
        return self._get_latest_posts(num_posts)

    def _get_latest_posts(self, num_posts):
        ''':return a list of post links '''
        post_links = []
        while len(post_links) <= num_posts:
            post_links += list(utils.flatten(self.parse_pages(num_posts)))

        start_time = time.time()
        pool = ThreadPool(4) # multithreading speed it up by 3x!
        posts = pool.map(Post, post_links[:num_posts])
        #posts = [Post(l) for l in post_links]
        print('Spend: %f secs to download the posts' % (time.time() - start_time))
        return posts

    def parse_pages(self, num_posts):
        ''':return a list of Post objects in this page'''
        num_viewed = 0
        while num_viewed <= num_posts:
            page = self._cur_page if self._cur_page else ""
            resp = agent.get(utils.make_ptt_url(domain, self.name, page))
            posts = self.parse_entry_links(resp)
            self._cur_page = self._get_next_link(resp)
            num_viewed += len(posts)
            print(f"number of post parsed: {num_viewed}")
            yield posts # newest post at the bottom

    def parse_entry_links(self, r: HTMLResponse):
        entries = r.html.find('div.r-ent')
        res = []
        for entry in entries:
            try:
                res.append(entry.find('div.title > a', first=True).attrs['href'])
            except IndexError:
                break
            except AttributeError:
                break
        return res
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

    def _get_next_link(self, r: HTMLResponse):
        html = HTML(html=r.text)
        page_controls = html.find('.action-bar a.btn.wide')
        prev_url = page_controls[1].attrs.get('href') # like '/bbs/Gossiping/index39400.html'
        return utils.get_page_index_from_href(prev_url)

class Post():
    def __init__(self, link):
        self.post_id = link
        self.title, self.category, self.country, self.author, self.votes, self.commentors = self.parse_post(link)

    def parse_post(self, link):
        url = urljoin(domain, link)
        resp = agent.get(url)

        try:

            main = resp.html.find('#main-content', first=True)
            title, category, country, author = self._parse_meta_and_post_line(main)
            votes, commentors = self._parse_comments(main)

        except IndexError:
            return None, None, None, None, None

        return title, category, country, author, votes, commentors

    def _parse_meta_and_post_line(self, main):
        metaline = main.find('div.article-metaline')
        ip_text = main.find('span', containing='發信站: 批踢踢實業坊(ptt.cc)', first=True).text
        ip, country = utils.parse_ip(ip_text)

        title = metaline[1].find('span')[1].text
        post_type = 'RE' if 'Re:' in title else 'OP'
        category = utils.get_cat_from_title(title)

        author_id = utils.get_user_handle(metaline[0].find('span')[1].text)
        datetime = metaline[2].find('span')[1].text
        author = Author(author_id, ip, datetime, post_type)

        return title, category, country, author

    def _parse_comments(self, main):
        REC_MAP = {
            "→": "neutral",
            "推": "pos",
            "噓": "neg"
        }
        votes = (dict([k,0] for k in ["counts", "pos", "neg", "neutral"]))
        commentors = []

        for push in main.find('div.push'):
            if push:
                # get vote stats
                votes['counts'] += 1
                rec_type = REC_MAP.get(push.find('span.push-tag', first=True).text)
                votes[rec_type] += 1
                # get commentors information
                push_uid = push.find('span.push-userid', first=True).text
                push_iptime = push.find('span.push-ipdatetime', first=True).text
                ip, comment_time = utils.parse_ip(push_iptime)  # dt looks like 10/12 05:39
                # make the timestamp consistent with post creation time
                try:
                    dt = datetime.strptime(comment_time, '%m/%d %H:%M')
                    dt = dt.replace(year=2019)
                    dt = dt.ctime()
                except ValueError:
                    dt = 'unknown'
                commentors.append(Commentor(push_uid, ip, dt, rec_type))

        votes['score'] = votes['pos'] - votes['neg']
        return votes, commentors

    def _parse_content(self):
        # TODO
        pass