import requests
import logging
import re
from bs4 import BeautifulSoup
from parsers.my_exceptions import page_not_found


class MediumParcer():
    """
    Парсинг информации о пользователе с medium
    """

    def get_url(self, tag):
        if tag[0] == '@':
            url = f'https://medium.com/{tag}'
        else:
            url = f'https://medium.com/@{tag}'
        return url

    def get_profile_html(self, url):

        try:
            responce = requests.get(url)
        except OSError:
            logger.exception(f'OSError: {url}')

        soup = BeautifulSoup(responce.text, 'html.parser')
        return soup

    def get_user_posts(self, soup):
        h1 = soup.findAll('h1')
        posts_href = []
        for tag in h1:
            href = tag.a['href']
            if href:
                if href[0] == '/':
                    posts_href.append(f'https://medium.com{href}')
                else:
                    posts_href.append(href)

        return posts_href

    def check_real_page(self, soup, tag):
        if soup.findAll(string='PAGE NOT FOUND'):
            raise page_not_found.PageNotFound(tag)

    def valid_url(self, tag):
        """
        Преобразует юзер тэг в ссылку и проверяет валидность ссылки
        :param tag:
        :return:
        """
        pattern = r'(https?://[^\"\s>]+)'

        if re.search(pattern, tag):
            pattern1 = r'medium\.com/@'
            pattern2 = r'\w+\.medium\.com'
            if re.search(pattern1, tag):
                return tag
            elif re.search(pattern2, tag):
                return tag
            else:
                return None
        else:
            return self.get_url(tag)

    def get_user_info(self, tag):
        """
        Получаем список постов пользователя
        :param tag: никнейм пользователя на сайте
        :return: ссылки на его статьи
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
        info['posts'] = self.get_user_posts(soup)

        return info


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)

    medium_parcer = MediumParcer()
    # print(medium_parcer.get_user_info('@zhll'))
    print(medium_parcer.get_user_info('https://medium.com/@zhlli'))


if __name__ == 'medium_parcer':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)