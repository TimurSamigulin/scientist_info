import os
import re
import io


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

    def get_info(self, text):
        """
        Функция конструктор
        :param text: текст с информацией о человеке
        :return:
        """
        emails = self.get_email(text)
        phones = self.get_phone(text)
        urls = self.get_url(text)

        name = 'Ahmadi Matthew N'
        print(self.find_fio(text, name))
        print(f'{emails}, {phones}, {urls}')


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
    file_path = 'data/foreign-dataset/Ahmadi Matthew N/0_www.umass.edu.txt'
    f = io.open(file_path)
    text = f.read()

    information = Information()
    # information.get_info(text)

    path = 'data/foreign-dataset'
    files = get_files(path)

    exit()
