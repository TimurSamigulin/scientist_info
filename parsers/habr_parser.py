import requests
import logging
from bs4 import BeautifulSoup

class HabrParser():
    """
    Класс для парсинга информации о пользователе с habr
    """
    def get_profile_html(self, url):
        """
        Получаем html код страницы
        :param url: ссылка на страницу
        :return: код страницы
        """

        try:
            responce = requests.get(url)
        except OSError:
            logger.exception(f'OSError: {url}')

        soup = BeautifulSoup(responce.text, 'html.parser')
        return soup

    def get_user_counters(self, soup):
        """
        Информация о рейтинге с профиля пользователя
        :param soup: код страницы
        :return: рейтинг и другие показатели пользователя
        """
        counters = {}

        counters['carma'] = soup.find(href="https://habr.com/ru/info/help/karma/").div.text
        counters['rating'] = soup.find(href="https://habr.com/ru/info/help/karma/#rating").div.text
        counters['followers'] = soup.find(href="https://habr.com/ru/users/pawnhearts/subscription/followers/").div.text
        counters['follow'] = soup.find(href="https://habr.com/ru/users/pawnhearts/subscription/follow/").div.text

        return counters

    def get_user_profile_summary(self, soup):
        """
        Информация о пользователе с его профиля
        :param soup: код страницы, soup с BeautifulSoup
        :return:
        """
        defination_list = soup.find('ul', 'defination-list')
        summary_li = defination_list.findAll('li')

        summary = {}
        for li in summary_li:
            summary[li.span.text] = li.find('span', 'defination-list__value').text

        return summary

    def get_user_posts(self, soup):
        """
        Ссылки на посты пользователя
        :param soup:
        :return:
        """

        posts = soup.find('div', 'posts_list').ul.findAll('li', 'content-list__item')

        posts_href = []
        for post in posts:
            posts_href.append(post.article.h2.a['href'])

        return posts_href

    def get_url(self, tag):
        """
        Формирует url на профиль пользователя
        :param tag: ник пользователя на хабр
        :return:
        """
        return f'https://habr.com/ru/users/{tag}'

    def get_user_info(self, tag):
        """
        Функция парсит основную информацию о пользователи на Хабр и его посты
        :param tag: никнейм на хабр
        :return: dict со всей найденной информацией
        """
        url = self.get_url(tag)
        soup = self.get_profile_html(url)

        info = {}
        counters = self.get_user_counters(soup)
        for k, v in counters.items():
            info[k] = v

        summary = self.get_user_profile_summary(soup)
        for k, v in summary.items():
            info[k] = v

        #меняем url, так как посты на другой странице
        url += '/posts/'
        soup = self.get_profile_html(url)
        info['posts'] = self.get_user_posts(soup)

        return info



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)

    habr_parser = HabrParser()
    print(habr_parser.get_user_info('VictoriaSeredina'))

if __name__ == 'habr_parser':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)