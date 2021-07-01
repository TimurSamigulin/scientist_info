import os
import re
import io
import logging

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
        pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
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

    def find_staff(self, text) -> dict:
        """
        Ищем должности\научные степени в тексте
        :param text: текст
        :return: dict -> title: bool
        """
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
        text = self.text_lower(text)
        for key in staff:
            staff[key] = self.find_word(text, key)

        return staff

    def text_token(self, text):
        """
        Токенизация текста по темам
        :param text: текст
        :return: список токенов по темам текста
        """
        from nltk.tokenize.texttiling import TextTilingTokenizer
        ttt = TextTilingTokenizer()
        theme_tokens = ttt.tokenize(text)
        logger.info(f'theme_token = {len(theme_tokens)}')
        return theme_tokens

    def check_info(self, text, fio):
        """
        Делит текст на токены структурно и возвращет только те в которых было совпадение по фио.
        :param text:
        :param fio:
        :return:
        """
        theme_tokens = self.text_token(text)
        have_info = []
        for token in theme_tokens:
            fio_dict = self.find_fio(token, fio)
            for name in fio_dict:
                if fio_dict[name]:
                    have_info.append(token)
                    break
        logger.info(f'have_info = {len(have_info)}')
        return have_info

    def check_title(self, text):
        pass


    def get_info(self, text, fio):
        """
        Функция конструктор
        :param text: текст с информацией о человеке
        :return:
        """

        emails = self.get_email(text)
        phones = self.get_phone(text)
        urls = self.get_url(text)
        staff = self.find_staff(text)
        have_info = self.check_info(text, fio)



        # print(self.check_info(text, 'Carroll Maria B'))
        # name = 'Ahmadi Matthew N'
        # print(self.find_fio(text, name))
        # print(f'{emails}, {phones}, {urls}')


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
            if file.split('.')[-1] in ['txt', 'pdf']:
                if files_dict.get(dir, False):
                    files_dict[dir].append(f'{path}/{dir}/{file}')
                else:
                    files_dict[dir] = [f'{path}/{dir}/{file}']

    return files_dict

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)

    information = Information()

    path = 'data/foreign-dataset'
    files = get_files(path)
    for name, path in files.items():
        for file in path:
            f = io.open(file)
            text = f.read()
            information.get_info(text, name)
            f.close()

    exit()
