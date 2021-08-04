import re
import json
from fastapi import FastAPI

from information_from_text.info import Information
from information_from_text.info_rus import InformationRus
from information_from_text.google_trans import GoogleTranslator
from bd.bd_adapter import BD_Adapter
from parsers.sites_text_parser import SitesParser
from parsers.papers_parser import PapersParser

app = FastAPI()


@app.get('/')
def index():
    return {'text_response': {'message': 'main page of scientist info'}}


def get_info(text, fio):
    """
    Функция для получения информации о человеке из текста для русского и английского языков
    :param text: Текст с сайта откуда мы хотим получить информацию о человеке
    :param fio: фио человека
    :return:
    """

    information_en = Information()
    information_ru = InformationRus()

    translator = GoogleTranslator()
    # Если текст русский, то переводим фио на русский
    rus = re.findall(r"[А-Яа-я]", text)
    if len(rus) > 30:
        if len(re.findall(r"[А-Яа-я]", fio)) > 1:
            fio = translator.translate_one(fio)
        info = information_ru.get_info(text, fio)
    else:
        info = information_en.get_info(text, fio)

    return info


@app.get('/get_info_from_text/')
def get_info_from_text(url: str, fio: str, scopus_author_id: int):
    """
    Функция для получения информации о человеке с сайта
    :param url: ссылка на сайт
    :param fio: фио человека
    :param scopus_author_id: scopus_author_id
    :return:
    """
    # Получаем текст страницы
    text = SitesParser.get_page_text(url)
    # Вытаскиваем информацию о человеке из текста
    info = get_info(text, fio)

    # подключаем адаптер для работы с базой
    with open('config', 'r') as cfg_file:
        config = json.load(cfg_file)
    adapter = BD_Adapter(config['database'], config['user'], config['password'], config['host'], config['port'])
    # Созраняем информацию о человеке в базу
    result = adapter.insert_info_from_text(url, info, fio, scopus_author_id)
    if result == 1:
        return {'text_response': {'message': f'Все отлично! Пользователь {fio} добавлен в базу'}}
    else:
        return {'text_response': {'message': f'Что-то не сохранилось в базу {info}'}}


@app.get('/parser_from_site/')
def parser_from_site(url: str, author_id: int):
    """
    Парсинг профилей пользователей для сайтов habr, vc ru, medium, papers_with_code
    :param url: ссылка на профиль пользователя
    :param author_id: id автора
    :return:
    """
    parser = PapersParser()

    # Подключаем адаптер для работы с базой
    with open('config', 'r') as cfg_file:
        config = json.load(cfg_file)
    adapter = BD_Adapter(config['database'], config['user'], config['password'], config['host'], config['port'])

    #Парсим в зависимости от сайта
    if 'habr' in url:
        try:
            habr_info = parser.get_habr_user_info(url)
        except AttributeError:
            return {'text_response': {
                'message': f'Видимо DOM у papers with code изменился, либо надо проверить ссылку {url}'}}
        if not habr_info:
            return {'text_response': {'message': f'Ничего не вернулось, возможно {url} ведет не на профиль или '
                                                 f'структура сайта сменилась'}}
        result = adapter.insert_author_info('habr', habr_info, author_id)
        if result:
            return {'text_response': {'message': f'Все отлично! Пользователь {url} добавлен в базу'}}
        else:
            return {'text_response': {'message': f'Что-то не так {url} не был добавлен в базу'}}

    elif 'medium' in url:
        try:
            medium_info = parser.get_medium_user_info(url)
        except AttributeError:
            return {'text_response': {
                'message': f'Видимо DOM у papers with code изменился, либо надо проверить ссылку {url}'}}

        if not medium_info:
            return {'text_response': {'message': f'Ничего не вернулось, возможно {url} ведет не на профиль или '
                                                 f'структура сайта сменилась'}}

        result = adapter.insert_author_info('medium', medium_info, author_id)
        if result:
            return {'text_response': {'message': f'Все отлично! Пользователь {url} добавлен в базу'}}
        else:
            return {'text_response': {'message': f'Что-то не так {url} не был добавлен в базу'}}
    elif 'vc.ru' in url:
        try:
            vr_ru_info = parser.get_vcru_user_info(url)
        except AttributeError:
            return {'text_response': {
                'message': f'Видимо DOM у papers with code изменился, либо надо проверить ссылку {url}'}}

        if not vr_ru_info:
            return {'text_response': {'message': f'Ничего не вернулось, возможно {url} ведет не на профиль или '
                                                 f'структура сайта сменилась'}}

        result = adapter.insert_author_info('vc', vr_ru_info, author_id)
        if result:
            return {'text_response': {'message': f'Все отлично! Пользователь {url} добавлен в базу'}}
        else:
            return {'text_response': {'message': f'Что-то не так {url} не был добавлен в базу'}}
    elif 'paperswithcode' in url:
        try:
            paper_info = parser.get_papers_with_code_info(url)
        except AttributeError:
            return {'text_response': {
                'message': f'Видимо DOM у papers with code изменился, либо надо проверить ссылку {url}'}}

        if not paper_info:
            return {'text_response': {'message': f'Ничего не вернулось, возможно {url} ведет не на профиль или '
                                                 f'структура сайта сменилась'}}

        result = adapter.insert_author_info('paper_with_code', paper_info, author_id)
        if result:
            return {'text_response': {'message': f'Все отлично! Пользователь {url} добавлен в базу'}}
        else:
            return {'text_response': {'message': f'Что-то не так {url} не был добавлен в базу'}}
    else:
        return {'text_response': {'message': f'Ссылка не релевантная {url}'}}
