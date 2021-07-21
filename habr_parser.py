import requests
import logging
from bs4 import BeautifulSoup

class HabrParser():
    """
    Класс для парсинга информации о пользователе с habr
    """
    def get_profile_html(self, url):

        try:
            responce = requests.get(url)
        except OSError:
            logger.exception(f'OSError: {url}')

        soup = BeautifulSoup(responce.text, 'html.parser')
        return soup

    def get_user_counters(self, soup):
        counters = {}

        counters['carma'] = soup.find(href="https://habr.com/ru/info/help/karma/").div.text
        counters['rating'] = soup.find(href="https://habr.com/ru/info/help/karma/#rating").div.text
        counters['followers'] = soup.find(href="https://habr.com/ru/users/pawnhearts/subscription/followers/").div.text
        counters['follow'] = soup.find(href="https://habr.com/ru/users/pawnhearts/subscription/follow/").div.text

        return counters

    def get_user_profile_summary(self, soup):
        defination_list = soup.find('ul', 'defination-list')
        summary_li = defination_list.findAll('li')

        summary = {}
        for li in summary_li:
            summary[li.span.text] = li.find('span', 'defination-list__value').text

        return summary

    def get_user_posts(self, url):
        url += '/posts/'
        soup = self.get_profile_html(url)

        posts = soup.find('div', 'posts_list').ul.findAll('li', 'content-list__item')

        posts_href = []
        for post in posts:
            posts_href.append(post.article.h2.a['href'])

        return posts_href

    def get_url(self, tag):
        return f'https://habr.com/ru/users/{tag}'

    def get_user_info(self, tag):
        url = self.get_url(tag)
        soup = self.get_profile_html(url)

        info = {}
        counters = self.get_user_counters(soup)
        for k, v in counters.items():
            info[k] = v

        summary = self.get_user_profile_summary(soup)
        for k, v in summary.items():
            info[k] = v

        info['posts'] = self.get_user_posts(url)

        return info



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)

    habr_parser = HabrParser()
    print(habr_parser.get_user_info('pawnhearts'))

if __name__ == 'habr_parser':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)