import requests
import logging
import re
from bs4 import BeautifulSoup
from parsers.my_exceptions import page_not_found

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

        counters['carma'] = soup.find('div', 'tm-karma__votes').text.strip()
        counters['rating'] = soup.find('div', 'tm-rating__counter').text.strip()
        # counters['followers'] = soup.find(href="https://habr.com/ru/users/pawnhearts/subscription/followers/").div.text
        # counters['follow'] = soup.find(href="https://habr.com/ru/users/pawnhearts/subscription/follow/").div.text

        return counters

    def get_user_profile_summary(self, soup):
        """
        Информация о пользователе с его профиля
        :param soup: код страницы, soup с BeautifulSoup
        :return:
        """
        defination_list = soup.find('div', 'tm-user-basic-info')
        summary_dl = defination_list.findAll('dl')

        summary = {}
        for dl in summary_dl:
            summary[dl.dt.text] = dl.dd.text.strip()

        return summary

    def get_user_posts(self, soup):
        """
        Ссылки на посты пользователя
        :param soup:
        :return:
        """

        posts = soup.find('div', 'tm-sub-page__main').findAll('article', 'tm-articles-list__item')

        posts_href = []
        for post in posts:
            post_url = 'https://habr.com' + post.div.h2.a['href']
            post_rating = post.find('span', 'tm-votes-meter__value').text
            posts_href.append({'url': post_url, 'rating': post_rating})

        return posts_href

    def get_url(self, tag):
        """
        Формирует url на профиль пользователя
        :param tag: ник пользователя на хабр
        :return:
        """
        return f'https://habr.com/ru/users/{tag}'

    def check_real_page(self, soup, tag):
        """
        Проверяем существование страницы пользователя
        :param soup: soup
        :param tag: юзер тэг
        :return: вызывается исключение PageNotFound, если страницы не существует
        """
        if soup.find('div', 'tm-error-message'):
            raise page_not_found.PageNotFound(tag)

    def valid_url(self, tag):
        """
        Преобразует юзер тэг в ссылку и проверяет валидность ссылки
        :param tag:
        :return:
        """
        pattern = r'(https?://[^\"\s>]+)'

        if re.search(pattern, tag):
            if tag[-1] == '/':
                tag = tag[:-1]
            url = tag.split('/')
            url = '/'.join(url[:-1])

            if url != 'https://habr.com/ru/users':
                return None

            return tag
        else:
            return self.get_url(tag)

    def get_user_info(self, tag):
        """
        Функция парсит основную информацию о пользователи на Хабр и его посты
        :param tag: никнейм на хабр или url
        :return: dict со всей найденной информацией
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
        info['profile_url'] = url

        counters = self.get_user_counters(soup)
        for k, v in counters.items():
            info[k] = v

        summary = self.get_user_profile_summary(soup)
        info['summary'] = summary
        # for k, v in summary.items():
        #     info[k] = v

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
    print(habr_parser.get_user_info('https://habr.com/ru/users/pawnhearts/'))
    # print(habr_parser.get_user_info('Victorieredina'))

if __name__ == 'habr_parser':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)