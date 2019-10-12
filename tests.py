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

    def test_get_user_handle(self):
        r1 = utils.get_user_handle("a15568 (玉米)")
        r2 = utils.get_user_handle("a15568 ()")
        r3 = utils.get_user_handle(None)
        self.assertEqual(r1, "a15568")
        self.assertEqual(r2, "a15568")
        self.assertEqual(r3, "")

    def test_parse_ip(self):
        txt = "※ 發信站: 批踢踢實業坊(ptt.cc), 來自: 223.137.204.135 (臺灣)"
        t2 = "10/12 21:53"
        ip, country = utils.parse_ip(txt)
        ip2, dt = utils.parse_ip(t2)
        self.assertEqual(ip, "223.137.204.135")
        self.assertEqual(country, "臺灣")
        #self.assertEqual(ip2, 'unknown')
        self.assertEqual(dt, "10/12 21:53")

