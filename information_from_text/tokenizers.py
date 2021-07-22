from nltk.tokenize.simple import LineTokenizer
from nltk.tokenize.texttiling import TextTilingTokenizer
from nltk.tokenize import BlanklineTokenizer

class Tokenizers():
    def theme_tokenize(self, text: str) -> list:
        """
        Токенизация текста по темам
        :param text: текст
        :return: список токенов по темам текста
        """

        ttt = TextTilingTokenizer()
        try:
            theme_tokens = ttt.tokenize(text)
        except ValueError:
            theme_tokens = [text]

        return theme_tokens

    def blank_tokenizer(self, text: str) -> list:
        """
        Токенизация по пустым строкам
        :param text:
        :return:
        """

        tokens = BlanklineTokenizer().tokenize(text)
        return tokens


    def line_token(self, text: str) -> list:
        """
        Токенизация по строкам, пустые строки выкидываем. Также приводит к нижнему регистру.
        :param text: текст
        :return: токены разделенные по строкам
        """

        tokens = LineTokenizer(blanklines='discard').tokenize(text)
        tokens = [token.strip() for token in tokens]

        return tokens
