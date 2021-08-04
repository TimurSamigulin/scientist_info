from fastapi import FastAPI
from bd.bd_adapter import BD_Adapter

from parsers.papers_parser import PapersParser

app = FastAPI()

@app.get('/')
def index():
    return {'text_response': {'message': 'main page of scientist info'}}


@app.get('/get_info_from_text/')
def get_info_from_text(url: str, fio: str, scopus_author_id: int):
    pass


@app.get('/parser_from_site/')
def parser_from_site(url: str, author_id: int):
    parser = PapersParser()
    adapter = BD_Adapter()

    if 'habr' in url:
        try:
            habr_info = parser.get_habr_user_info(url)
        except AttributeError as a:
            return {'text_response': {'message': f'Видимо DOM у papers with code изменился, либо надо проверить ссылку {url}'}}

        adapter.insert_author_info('habr', habr_info, author_id)
        return {'text_response': {'message': f'Все отлично! Пользователь {url} добавлен в базу'}}
    elif 'medium' in url:
        try:
            medium_info = parser.get_medium_user_info(url)
        except AttributeError as a:
            return {'text_response': {'message': f'Видимо DOM у papers with code изменился, либо надо проверить ссылку {url}'}}

        adapter.insert_author_info('medium', medium_info, author_id)
        return {'text_response': {'message': f'Все отлично! Пользователь {url} добавлен в базу'}}
    elif 'vc.ru' in url:
        try:
            vr_ru_info = parser.get_vcru_user_info(url)
        except AttributeError as a:
            return {'text_response': {'message': f'Видимо DOM у papers with code изменился, либо надо проверить ссылку {url}'}}

        adapter.insert_author_info('vc', vr_ru_info, author_id)
        return {'text_response': {'message': f'Все отлично! Пользователь {url} добавлен в базу'}}
    elif 'paperswithcode' in url:
        try:
            paper_info = parser.get_papers_with_code_info(url)
        except AttributeError as a:
            return {'text_response': {'message': f'Видимо DOM у papers with code изменился, либо надо проверить ссылку {url}'}}

        adapter.insert_author_info('paper_with_code', paper_info, author_id)
        return {'text_response': {'message': f'Все отлично! Пользователь {url} добавлен в базу'}}
    else:
        return {'text_response': {'message': f'Ссылка не релевантная {url}'}}

