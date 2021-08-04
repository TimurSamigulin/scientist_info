from information_from_text.info import Information
import logging
import os
import io
import re

class InformationRus(Information):

    def find_depart(self, tokens):
        """
        Find Department
        :param tokens: токены по линиям
        :return: факультет
        """
        for token in tokens:
            if ('факультет' in token) or ('факультета' in token):
                return token

    def find_facult(self, tokens):
        for token in tokens:
            if 'кафедра' in token:
                return token

    def get_staff(self, text):
        staff = {
            'кандидат технических наук': False,
            'кандидат наук': False,
            'доктор наук': False,
            'доктор технических наук': False,
            'доцент': False,
            'профессор': False,
            'магистр': False,
            'phd': False,
            'бакалавр': False,
            'лаборант': False,
            'старший лаборант': False,
            'ассистент': False,
            'преподаватель': False,
            'старший преподаватель': False,
            'завкафедрой': False,
            'декан': False,
            'проректор': False,
            'ректор': False
        }

        return self.find_staff(text, staff)

    def get_section(self, tokens):
        sections = ['ученое звание', 'ученая степень', 'должность', 'служебные обязанности', 'образование',
                    'квалификации', 'деятельность', 'интересы', 'награды', 'хобби', 'биография', 'публикации',
                    'проекты', 'организация', 'профессия']
        return self.check_section(tokens, sections)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)


    exit()

if __name__ == 'info_rus':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)