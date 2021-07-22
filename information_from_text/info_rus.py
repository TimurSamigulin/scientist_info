from information_from_text.info import Information
import logging
import os
import io
import re
from information_from_text.info import get_files

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


def write_info(files, outputpath):
    """
    получаем инфо со страницы и запись в файл
    :param files:
    :return:
    """
    for name, path in files.items():
        logger.info(f'name = {name}')
        for file in path:
            f = io.open(file, encoding='utf-8')
            text = f.read()

            dirpath = outputpath + name

            if not os.path.exists(dirpath):
                os.makedirs(dirpath)

            rus = re.findall(r"[А-Яа-я]", text)
            if len(rus) > 30:
                info = information_rus.get_info(text, name)
            else:
                info = information.get_info(text, name)

            wpath = dirpath + '/' + file.split('/')[-1]
            with open(wpath, 'w', encoding='utf-8') as fw:
                for key, item in info.items():
                    if (item != 'None') or (item.strip() != ''):
                        fw.write(f"{key}:\n{item}\n")

            f.close()
            fw.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)

    information = Information()
    information_rus = InformationRus()

    path = '../data/ru-4'
    files = get_files(path)
    write_info(files, 'data/output-ru-4/')

    exit()

if __name__ == 'info_rus':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)