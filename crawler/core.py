# -*- coding: utf-8 -*-

from requests_html import HTML, HTMLSession
import parser
import utils

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

class Board():
    def __init__(self, name):
        self.name = name
        self._cur_page = None

    def get_post_list(self, num_posts):

        return self._get_latest_posts(num_posts)

    def _get_latest_posts(self, num_posts):
        ''':return a list of Ariticle obj'''
        article_links = []
        while True:
            article_links += self.parse_pages(num_posts)
            if len(article_links) >= num_posts:
                break
        return article_links[:num_posts]
        #return [Article(l) for l in article_links]

    def parse_pages(self, num_posts):
        ''':return a list of Ariicle obj in this page'''
        num_viewed = 0

        while True:
            page = self._cur_page if self._cur_page else ""
            resp = agent.get(utils.make_ptt_url(domain, self.name, page))
            posts = [parser.parse_entry_meta(resp.html.find('div.r-ent'))]
            self._cur_page = parser.get_next_link(resp)
            yield posts # newest post at the bottom

            num_viewed += len(posts)
            if num_posts and num_viewed > num_posts:
                break

class Article():
    def __init__(self, url):
        self.url = url

    def get_comments(self):
        pass

    def get_voters(self):
        pass



if __name__ == "__main__":
    agent = Agent()
    print("init...")
    b = Board("Gossiping")
    posts = b.get_post_list(20)
    print(list(posts))