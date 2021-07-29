class PageNotFound(Exception):
    """
    Класс исключения для случая, когда страница пользователя не найдена
    """
    def __init__(self, user, message="Данный пользователь не найден"):
        """
        Страница пользователя не найдена
        :param user: юзер тэг
        :param message: сообщения для вывода в консоль
        """
        self.user = user
        self.message = message
        super().__init__(self.message)

    # переопределяем метод '__str__'
    def __str__(self):
        return f'{self.user} -> {self.message}'