from bd.sql_connector import Connector


class BD_Adapter():
    """
    Адаптер для работы с базы
    """

    def __init__(self, db_name, user, password, host, port):
        self.__db_name = db_name
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port
        self.db_connection = Connector(self.__db_name, self.__user, self.__password, self.__host, self.__port)

    def insert_author_info(self, site, info, author_id):
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

        # Записываем инфу о пользователе
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

        id = self.db_connection.insert_data(table_name, columns, values)

        # Вставляем посты
        if info.get('posts', False):
            posts = info.get('posts')
        elif info.get('papers_url', False):
            posts = info.get('papers_url')
        else:
            return 1

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
            self.db_connection.insert_data(table_name_post, posts_columns, post)

        return 1

    def insert_info_from_text(self, url, info, fio, scopus_author_id):
        table_scopus_author_info = 'scopus_author_info'
        table_scopus_author_email = 'scopus_author_email'
        table_scopus_author_phone = 'scopus_author_phone'
        table_scopus_author_url = 'scopus_author_url'

        all_columns = ['depart', 'faculty', 'designation', 'teaching_area', 'book_chapter', 'research', 'membership',
                       'employment', 'overview',
                       'qualification', 'about_me', 'contact', 'biography', 'journals', 'conferences', 'publications',
                       'staff', 'info']
        columns = ['scopus_author_id', 'url']
        values = [scopus_author_id, url]

        for column in all_columns:
            if info.get(column, 0):
                columns.append(column)
                values.append(info.get(column))

        columns = tuple(columns)
        values = tuple(values)

        id = self.db_connection.insert_data(table_scopus_author_info, columns, values)

        if info.get('emails', 0):
            emails = info.get('emails').split(';')
            columns = (
                'author_info_id',
                'email'
            )
            values = []
            for email in emails:
                values.append((id, email))

            if len(values) > 0:
                for value in values:
                    self.db_connection.insert_data(table_scopus_author_email, columns, value)

        if info.get('phones', 0):
            phones = info.get('phones').split(';')
            columns = (
                'author_info_id',
                'phone'
            )
            values = []
            for phone in phones:
                values.append((id, phone))

            if len(values) > 0:
                for value in values:
                    self.db_connection.insert_data(table_scopus_author_phone, columns, value)

        if info.get('urls', 0):
            urls = info.get('urls').split(';')
            columns = (
                'author_info_id',
                'url'
            )
            values = []
            for url in urls:
                values.append((id, url))

            if len(values) > 0:
                for value in values:
                    self.db_connection.insert_data(table_scopus_author_url, columns, value)

        return 1
