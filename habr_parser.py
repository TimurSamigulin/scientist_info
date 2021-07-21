import requests
import logging
import re
from bs4 import BeautifulSoup

class HabrParser():
    """
    Класс для парсинга информации о пользователе с habr
    """
    def get_profile_html(self, tag):
        url = f'https://habr.com/ru/users/{tag}'

        try:
            responce = requests.get(url)
        except OSError:
            logger.exception(f'OSError: {url}')

        soup = BeautifulSoup(responce.text, 'html.parser')
        return soup

    def get_user_counters(self, soup):
        carma = soup.find(href="https://habr.com/ru/info/help/karma/").div.text
        rating = soup.find(href="https://habr.com/ru/info/help/karma/#rating").div.text
        followers = soup.find(href="https://habr.com/ru/users/pawnhearts/subscription/followers/").div.text
        follow = soup.find(href="https://habr.com/ru/users/pawnhearts/subscription/follow/").div.text

    def get_user_profile_summary(self, soup):
        defination_list = soup.find('ul', 'defination-list')
        summary_li = defination_list.findAll('li')

        summary = {}
        for li in summary_li:
            summary[li.span.text] = li.find('span', 'defination-list__value').text

        return summary


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)

    habr_parser = HabrParser()
    soup = habr_parser.get_profile_html('pawnhearts')

    # print(soup.findAll(href=re.compile("https://habr.com/ru/info/help/karma/")))