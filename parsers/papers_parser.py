import logging
from parsers.habr_parser import HabrParser
from parsers.medium_parcer import MediumParcer
from parsers.vc_ru_parser import VcRuParser
from parsers.papers_with_code_parser import PapersWithCodeParser

class PapersParser():

    def get_habr_user_info(self, tag):
        habr_parser = HabrParser()
        user_info = habr_parser.get_user_info(tag)
        return user_info

    def get_medium_user_info(self, tag):
        medium_parser = MediumParcer()
        user_info = medium_parser.get_user_info(tag)
        return user_info

    def get_vcru_user_info(self, tag):
        vcru_parser = VcRuParser()
        user_info = vcru_parser.get_user_info(tag)
        return user_info

    def get_papers_with_code_info(self, tag):
        papers_with_code = PapersWithCodeParser()
        user_info = papers_with_code.get_user_info(tag)
        return user_info

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)

    papers_parser = PapersParser()
    print(papers_parser.get_habr_user_info('VictoriaSeredina'))
    print(papers_parser.get_medium_user_info('@zhlli'))
    print(papers_parser.get_vcru_user_info('781084-masha-cepeleva'))
    print(papers_parser.get_papers_with_code_info('Oriol Vinyals'))