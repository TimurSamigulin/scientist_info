from fastapi import FastAPI

from parsers.papers_parser import PapersParser

app = FastAPI()

@app.get('/')
def index():
    return {'text_response': {'message': 'main page of scientist info'}}

@app.get('/parser_from_site/')
def parser_from_site(url: str):
    parser = PapersParser()
    if 'habr' in url:
        try:
            habr_info = parser.get_habr_user_info(url)
        except AttributeError as a:
            return {'text_response': {'message': f'Видимо DOM у papers with code изменился, либо надо проверить ссылку {url}'}}
    elif 'medium' in url:
        try:
            medium_info = parser.get_medium_user_info(url)
        except AttributeError as a:
            return {'text_response': {'message': f'Видимо DOM у papers with code изменился, либо надо проверить ссылку {url}'}}
    elif 'vc.ru' in url:
        try:
            vr_ru_info = parser.get_vcru_user_info(url)
        except AttributeError as a:
            return {'text_response': {'message': f'Видимо DOM у papers with code изменился, либо надо проверить ссылку {url}'}}
    elif 'paperswithcode' in url:
        try:
            paper_info = parser.get_papers_with_code_info(url)
        except AttributeError as a:
            return {'text_response': {'message': f'Видимо DOM у papers with code изменился, либо надо проверить ссылку {url}'}}
    else:
        return {'text_response': {'message': f'Ссылка не релевантная {url}'}}

