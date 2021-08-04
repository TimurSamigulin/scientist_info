from bd.sql_connector import Connector

class BD_Adapter():

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
