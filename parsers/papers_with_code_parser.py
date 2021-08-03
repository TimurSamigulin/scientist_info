import requests
import logging
import re
from bs4 import BeautifulSoup

class PapersWithCodeParser():

    def get_url(self, name):
        name = str.replace(name, ' ', '+')
        url = f'https://paperswithcode.com/search?q=author%3A{name}'
        return url

    def get_profile_html(self, url):

        try:
            responce = requests.get(url)
        except OSError:
            logger.exception(f'OSError: {url}')

        soup = BeautifulSoup(responce.text, 'html.parser')
        return soup

    def get_user_counters(self, soup):
        counters = soup.find('h3', 'home-page-subtitle').findAll('b')
        papers = counters[0].text
        papers_code = counters[1].text
        return papers, papers_code

    def get_user_papers(self, soup):
        papers = soup.findAll('div', 'entity') # Для извлечения ссылок на статьи
        papers_rating = soup.findAll('div', 'entity-stars') # Для извлечения рейтинга статей

        papers_href = []
        for i, paper in enumerate(papers):
            post_url = 'https://paperswithcode.com' + paper.find('a')['href']
            post_rating = papers_rating[i].text.strip().replace(',', '')
            if post_rating == '':
                post_rating = 0
            else:
                post_rating = int(post_rating)
            papers_href.append({'url': post_url, 'rating': post_rating})

        return papers_href

    def valid_url(self, tag):
        """
        Преобразует юзер тэг в ссылку и проверяет валидность ссылки
        :param tag:
        :return:
        """
        pattern = r'(https?://[^\"\s>]+)'

        if re.search(pattern, tag):
            pattern = r'author'
            if re.search(pattern, tag):
                return tag
            else:
                return None
        else:
            return self.get_url(tag)

    def get_user_info(self, tag):
        """
        Получаем основную информацию о пользователе с сайта papers with parser и ссылки на статьи
        :param tag: ник на сайте
        :return: словарь с основной инфой
        """
        url = self.valid_url(tag)
        if not url:
            return None

        soup = self.get_profile_html(url)

        info = {}
        info['url'] = url
        papers, papers_code = self.get_user_counters(soup)
        info['papers'] = int(papers)
        info['papers_with_code'] = int(papers_code)
        info['papers_url'] = self.get_user_papers(soup)

        return info


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)

    papers_parser = PapersWithCodeParser()
    print(papers_parser.get_user_info('Oriol Vinyals'))


if __name__ == 'papers_with_code_parcer':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)

