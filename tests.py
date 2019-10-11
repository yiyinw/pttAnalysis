import unittest

from crawler.parser import get_page_index_from_href
from crawler import utils

class TestParser(unittest.TestCase):
    def test_page_index_parser_normal(self):
        """
        :return: it returns page index
        """
        r = get_page_index_from_href('/bbs/Gossiping/index39400.html')
        self.assertEqual(r, "39400")

    def test_page_index_parser_empty(self):
        """
        :return: it returns page index
        """
        r = get_page_index_from_href('/bbs/Gossiping/index.html')
        self.assertEqual(r, None)

class TestUtils(unittest.TestCase):
    def test_make_url(self):
        r = utils.make_ptt_url('https://ptt.cc', 'movie', '39400')
        self.assertEqual(r, 'https://ptt.cc/bbs/movie/index39400.html')
