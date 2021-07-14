import os
import re
import io
import logging
from nltk.tokenize.simple import LineTokenizer
from nltk.tokenize.texttiling import TextTilingTokenizer


class Information:
    """
    Класс для получения информации о пользователе из текста
    """

    def get_email(self, text) -> list:
        """
        Функция для получения email из текста
        :param text: текст
        :return: list emails
        """

        pattern = r'[\w\.-]+@[\w\.-]+'
        emails = re.findall(pattern, text)
        return emails

    def get_phone(self, text) -> list:
        """
        Функция для получения номеров телефона из текста
        :param text: текст
        :return: list номеров
        """

        pattern = r'[\+\(]?[1-9][0-9 \-\(\)]{8,22}[0-9]'
        phones = re.findall(pattern, text)
        return phones

    def get_url(self, text) -> list:
        """
        Функция для получения url из текста
        :param text: текст
        :return: list URLs
        """

        pattern = r'(https?://[^\"\s>]+)'
        urls = re.findall(pattern, text)
        return urls

    def text_lower(self, text: str):
        """
        Приведит текст к нижнему регистру
        :param text: текст
        :return: текст в нижнем регистре
        """

        return text.lower()

    def find_fio(self, text: str, fio: str) -> dict:
        """
        Функция, которая ищет наличие fio в тексте.
        :param text: текст
        :param fio: фио
        :return: словарь с именем и True если найдено, False не найдено
        """

        fio = [name for name in fio.split(' ') if len(name) > 2]
        fio_dict = {}
        if text.find(' '.join(fio)) == -1:
            fio_dict[' '.join(fio)] = False
        else:
            fio_dict[' '.join(fio)] = True

        for name in fio:
            if text.find(name) == -1:
                fio_dict[name] = False
            else:
                fio_dict[name] = True

        return fio_dict

    def find_word(self, text: str, word: str):
        """
        Ищем наличия слова в биографии
        :param text: текст
        :param word: слово
        :return: возвращем bool найденно или нет, и позицию вхождения, -1 если не найденно
        """

        pos = text.find(word)
        if pos == -1:
            return False, pos
        else:
            return True, pos

    def line_token(self, text):
        """
        Токенизация по строкам, пустые пропускаем
        :param text: текст
        :return: токены
        """
        text = self.text_lower(text)
        tokens = LineTokenizer(blanklines='discard').tokenize(text)
        tokens = [token.strip() for token in tokens]


        return tokens

    def find_depart(self, tokens):
        """
        Find Department
        :param tokens: токены по линиям
        :return: факультет
        """
        for token in tokens:
            if 'department of' in token:
                return token

    def find_facult(self, tokens):
        """
        Find facult
        :param tokens: токены по линиям
        :return: факультеты
        """
        for token in tokens:
            if 'faculty of' in token:
                return token

    def find_univer_info(self, text):
        """
        Информация об университете, факультет и кафедра
        :param text: текст
        :return: факультет, кафедра
        """
        text = self.text_lower(text)
        tokens = self.line_token(text)
        depart = self.find_depart(tokens)
        facult = self.find_facult(tokens)
        return depart, facult

    def find_staff(self, text, staff):
        """
        Ищем должности\научные степени в тексте
        :param text: текст
        :return: dict -> title: bool
        """

        text = self.text_lower(text)
        for key in staff:
            staff[key] = self.find_word(text, key)[0]

        res_staff = []
        for key, items in staff.items():
            if items:
                res_staff.append(key)

        return res_staff

    def get_staff(self, text):
        staff = {
            'postgraduate': False,
            'dean': False,
            'director': False,
            'doctoral candidate': False,
            'associate professor': False,
            'assoc. prof.': False,
            'docent': False,
            'head of department': False,
            'research assistant': False,
            'research officer': False,
            'full professor': False,
            'lecturer': False,
            'professor': False,
            'applicant': False,
            'senior research officer': False,
            'assistant professor': False,
            'senior lecturer': False,
            'rector': False,
            'deputy rector': False,
            'chancellor': False,
            'vice-chancellor': False,
            'president': False,
            'vice-president': False,
            'ph.d.': False,
            'advanced doctor': False,
        }

        return self.find_staff(text, staff)

    def text_token(self, text):
        """
        Токенизация текста по темам
        :param text: текст
        :return: список токенов по темам текста
        """

        ttt = TextTilingTokenizer()
        try:
            theme_tokens = ttt.tokenize(text)
            logger.info(f'theme_token = {len(theme_tokens)}')
        except ValueError:
            theme_tokens = [text]

        return theme_tokens

    def check_info(self, theme_tokens, fio):
        """
        Делит текст на токены структурно и возвращет только те в которых было совпадение по фио.
        :param theme_tokens: тематические токены
        :param fio: фамилия имя очество
        :return:
        """

        have_info = []
        for token in theme_tokens:
            fio_dict = self.find_fio(token, fio)
            for name in fio_dict:
                if fio_dict[name]:
                    have_info.append(token)
                    break
        logger.info(f'have_info = {len(have_info)}')
        return have_info


    def check_section(self, tokens, sections):
        """
        Ищем в тексте секции, разделы
        :param tokens: токены
        :return: найденые разделы, секции и их текст
        """

        info = {}
        for sec_index, section in enumerate(sections):
            for tok_index, token in enumerate(tokens):
                if section in token:
                    if info.get(section, False):
                        try:
                            info[section] += '\n' + tokens[tok_index + 1]
                        except IndexError:
                            info[section] += '\n' + tokens[tok_index]
                    else:
                        try:
                            info[section] = tokens[tok_index + 1]
                        except IndexError:
                            info[section] = tokens[tok_index]

        return info

    def get_section(self, tokens):
        sections = ['designation', 'teaching area', 'conferences', 'journals', 'book chapter', 'research', 'membership', 'employment',
                    'overview', 'qualification', 'about me', 'contact', 'biography', 'publications']
        return self.check_section(tokens, sections)

    def get_section_info(self, text):
        """
        Токенизируем текст и Ищем в тексте секции, разделы
        :param tokens: текст
        :return: найденые разделы, секции и их текст
        """
        tokens = self.line_token(text)
        info = self.get_section(tokens)

        return info


    def get_info(self, text, fio):
        """
        Функция конструктор
        :param text: текст с информацией о человеке
        :return:
        """
        info = {}

        theme_tokens = self.text_token(text)

        info['emails'] = ' '.join(self.get_email(text))
        info['phones'] = ' '.join(self.get_phone(text))
        info['urls'] = ' '.join(self.get_url(text))

        depart, faculty = self.find_univer_info(text)
        info['depart'] = depart
        info['faculty'] = faculty

        section_info = self.get_section_info('\n'.join(theme_tokens))
        for key, item in section_info.items():
            info[key] = item

        info['staff'] = ' '.join(self.get_staff('\n'.join(theme_tokens)))

        info['info'] = ' '.join(self.check_info(theme_tokens, fio))

        return info


def get_files(path):
    """
    Получаем список файлов с информацией об ученых
    :param path: путь до нужной директории с папками ученых
    :return: словарь ученный: list файлов с информацией
    """

    dirs = os.listdir(path=path)

    files_dict = {}
    for dir in dirs:
        files = os.listdir(path=path + '/' + dir)
        for file in files:
            if file.split('.')[-1] in ['txt']:
                if files_dict.get(dir, False):
                    files_dict[dir].append(f'{path}/{dir}/{file}')
                else:
                    files_dict[dir] = [f'{path}/{dir}/{file}']

    return files_dict


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

    path = 'data/english_new'
    files = get_files(path)
    write_info(files, 'data/output-eng-new-test/')

    exit()

if __name__ == 'info':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)