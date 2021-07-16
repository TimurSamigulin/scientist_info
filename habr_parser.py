import requests
import logging
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)

    habr_parser = HabrParser()
    soup = habr_parser.get_profile_html('pawnhearts')
    print(soup.findAll(href='user-info__stats-item'))