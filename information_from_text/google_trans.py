from googletrans import Translator

class GoogleTranslator:

    translator = Translator()

    def translate_one(self, text):
        """
        Функция для перевода строки с англ на русский
        :param text: текст который нужно перевести
        :return: переведенный текст
        """
        translate_text = self.translator.translate(text, dest='ru', src='en').text
        return translate_text
