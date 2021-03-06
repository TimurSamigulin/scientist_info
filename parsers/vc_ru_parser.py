import requests
import logging
import json
import re
from bs4 import BeautifulSoup
from parsers.my_exceptions import page_not_found

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
        summary['karma'] = int(info['subsiteData']['karma'])
        summary['count'] = int(info['subsiteData']['subscribers']['count'])
        summary['label'] = info['stats'][0]['label']
        summary['posts_counter'] = int(info['tabs'][0]['counter'])

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
            post_rating = post.find('span', 'vote__value__v').text
            post_url = post.find('a', 'content-feed__link')['href']

            if post_rating == '—':
                post_rating = 0

            posts_href.append({'url': post_url, 'rating': int(post_rating)})

        return posts_href

    def check_real_page(self, soup, tag):
        """
        Проверяем существование страницы пользователя
        :param soup: soup
        :param tag: юзер тэг
        :return: вызывается исключение PageNotFound, если страницы не существует
        """
        if soup.find('div', 'error__code'):
            raise page_not_found.PageNotFound(tag)

    def valid_url(self, tag):
        """
        Преобразует юзер тэг в ссылку и проверяет валидность ссылки
        :param tag:
        :return:
        """
        pattern = r'(https?://[^\"\s>]+)'

        if re.search(pattern, tag):
            pattern = r'vc\.ru/u/'
            if re.search(pattern, tag):
                return tag
            else:
                return None
        else:
            return self.get_url(tag)


    def get_user_info(self, tag):
        """
        Получаем информацию о пользователи и его посты
        :param tag: ник пользователя на сайте vc_ru
        :return: Основная информация с профиля и ссылки на статьи
        """
        url = self.valid_url(tag)
        if not url:
            return None

        soup = self.get_profile_html(url)

        try:
            self.check_real_page(soup, tag)
        except page_not_found.PageNotFound:
            logger.info(f'Страница пользователя {tag} не найдена')
            return None

        info = {}
        info['url'] = url
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
    # print(vc_ru_parser.get_user_info('71man'))
    print(vc_ru_parser.get_user_info('https://vc.ru/u/781084-masha-cepeleva/'))


if __name__ == 'vc_ru_parser':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)