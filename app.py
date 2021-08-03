from fastapi import FastAPI

from parsers.papers_parser import PapersParser
from bd.sql_connector import Connector

app = FastAPI()

@app.get('/')
def index():
    return {'text_response': {'message': 'main page of scientist info'}}

def insert_into_bd(site, info, author_id):
    if site == 'habr':
        table_name = 'scopus_author_habr'
        table_name_post = 'scopus_author_habr_post'
    elif site == 'medium':
        table_name = 'scopus_author_medium'
        table_name_post = 'scopus_author_medium_post'
    elif site == 'vc':
        table_name = 'scopus_author_vc'
        table_name_post = 'scopus_author_vc_post'
    elif site == 'paper_with_code':
        table_name = 'scopus_author_paper_with_code'
        table_name_post = 'scopus_author_paper_with_code_url'
    else:
        return


    #Конектимся к бд
    db_config = dict(
        user='root',
        password='example',
        host='10.7.4.10',
        port=3306,
        database='exclusive'
    )

    db_connection = Connector(db_config['database'], db_config['user'], db_config['password'], db_config['host'],
                              db_config['port'])
    #Записываем инфу о пользователе
    columns = ['scopus_author_id']
    values = [author_id]

    all_columns = [
        'url',
        'carma',
        'rating',
        'rating_place',
        'location',
        'job',
        'birthday',
        'registered',
        'last_activity',
        'name',
        'karma',
        'count',
        'label',
        'posts_counter',
        'papers',
        'papers_with_code'
    ]
    for column in all_columns:
        if info.get(column, 0):
            columns.append(column)
            values.append(info.get(column))

    columns = tuple(columns)
    values = tuple(values)

    id = db_connection.insert_data(table_name, columns, values)

    # Вставляем посты
    if info.get('posts', False):
        posts = info.get('posts')
    elif info.get('papers_url', False):
        posts = info.get('papers_url')
    else:
        return

    id_name = f'{site}_id'
    if isinstance(posts[0], dict):
        posts_value = []
        posts_columns = (
            id_name,
            'url',
            'rating'
        )

        for post in posts:
            posts_value.append((id, post['url'], post['rating']))
    else:
        posts_value = []
        posts_columns = (
            id_name,
            'url'
        )
        for post in posts:
            posts_value.append((id, post))
    for post in posts_value:
        db_connection.insert_data(table_name_post, posts_columns, post)



@app.get('/parser_from_site/')
def parser_from_site(url: str, author_id: int):
    parser = PapersParser()
    if 'habr' in url:
        try:
            habr_info = parser.get_habr_user_info(url)
        except AttributeError as a:
            return {'text_response': {'message': f'Видимо DOM у papers with code изменился, либо надо проверить ссылку {url}'}}

        insert_into_bd('habr', habr_info, author_id)
        return {'text_response': {'message': f'Все отлично! Пользователь {url} добавлен в базу'}}
    elif 'medium' in url:
        try:
            medium_info = parser.get_medium_user_info(url)
        except AttributeError as a:
            return {'text_response': {'message': f'Видимо DOM у papers with code изменился, либо надо проверить ссылку {url}'}}

        insert_into_bd('medium', medium_info, author_id)
        return {'text_response': {'message': f'Все отлично! Пользователь {url} добавлен в базу'}}
    elif 'vc.ru' in url:
        try:
            vr_ru_info = parser.get_vcru_user_info(url)
        except AttributeError as a:
            return {'text_response': {'message': f'Видимо DOM у papers with code изменился, либо надо проверить ссылку {url}'}}

        insert_into_bd('vc', vr_ru_info, author_id)
        return {'text_response': {'message': f'Все отлично! Пользователь {url} добавлен в базу'}}
    elif 'paperswithcode' in url:
        try:
            paper_info = parser.get_papers_with_code_info(url)
        except AttributeError as a:
            return {'text_response': {'message': f'Видимо DOM у papers with code изменился, либо надо проверить ссылку {url}'}}

        insert_into_bd('paper_with_code', paper_info, author_id)
        return {'text_response': {'message': f'Все отлично! Пользователь {url} добавлен в базу'}}
    else:
        return {'text_response': {'message': f'Ссылка не релевантная {url}'}}

