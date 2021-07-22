import requests
import logging
from bs4 import BeautifulSoup
import json

class VcRuParser():

    def get_url(self, tag):
        """
        Формируем ссылку на профиль
        :param tag: никнейм на сайте
        :return:
        """
        return f'https://vc.ru/u/{tag}'

    def get_profile_html(self, url):
        """
        Код страницы
        :param url: ссылка на страницу
        :return:
        """
        try:
            responce = requests.get(url)
        except OSError:
            logger.exception(f'OSError: {url}')

        soup = BeautifulSoup(responce.text, 'html.parser')
        return soup

    def get_user_profile_summary(self, soup):
        """
        Основная информация из профиля пользователя
        :param soup:
        :return:
        """
        summary = {}

        info = soup.find('div', 'l-page__header').textarea.text
        info = json.loads(info)['header']

        summary['name'] = info['subsiteData']['name']
        summary['karma'] = info['subsiteData']['karma']
        summary['count'] = info['subsiteData']['subscribers']['count']
        summary['label'] = info['stats'][0]['label']
        summary['posts_counter'] = info['tabs'][0]['counter']

        return summary

    def get_user_posts(self, soup):
        """
        Возвращает ссылки на посты пользователя
        :param soup:
        :return:
        """
        posts = soup.findAll('div', 'feed__item l-island-round')
        posts_href = []
        for post in posts:
            posts_href.append(post.find('a', 'content-feed__link')['href'])

        return posts_href

    def get_user_info(self, tag):
        """
        Получаем информацию о пользователи и его посты
        :param tag: ник пользователя на сайте vc_ru
        :return: Основная информация с профиля и ссылки на статьи
        """
        url = self.get_url(tag)
        soup = self.get_profile_html(url)

        info = {}
        summary = self.get_user_profile_summary(soup)
        for k, v in summary.items():
            info[k] = v

        info['posts'] = self.get_user_posts(soup)

        return info


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)

    vc_ru_parser = VcRuParser()
    print(vc_ru_parser.get_user_info('781084-masha-cepeleva'))


if __name__ == 'vc_ru_parser':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)