import requests
import logging
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
        papers = soup.findAll('div', 'entity')
        papers_href = []
        for paper in papers:
            href = 'https://paperswithcode.com' + paper.find('a')['href']
            papers_href.append(href)

        return papers_href

    def get_user_info(self, tag):
        url = self.get_url(tag)
        soup = self.get_profile_html(url)

        info = {}
        info['tag'] = tag
        papers, papers_code = self.get_user_counters(soup)
        info['papers'] = papers
        info['papers_with_code'] = papers_code
        info['papers_url'] = self.get_user_papers(soup)

        return info


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)

    papers_parser = PapersWithCodeParser()
    print(papers_parser.get_user_info('Oriol Vinyals'))

