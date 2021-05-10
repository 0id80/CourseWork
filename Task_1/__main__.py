from os.path import isfile


class TextParser:
    def __init__(self, source):
        self.source_text = source

    def check_source_type(self) -> list:
        """
        Функция проверяет тип поданного аргумента
        Если аргумент = названию файла и файл существует
            Чтение файла, запись в переменную и возврат списка слов
        Если аргумент = строка - просто возвращает список слов разделённые методом split()
        """
        text = self.source_text
        if isfile(text):
            with open(text, "r", encoding="UTF-8") as file:
                text = file.read().split()
            return text
        else:
            return text.split()

    def count_and_sort(self) -> list:
        """
        Получение списка слов без повторений
        Подсчёт слов методом count() и добавление кортежа состоящего из частоты встречаемости и самого слова
        Первая сортировка нужна для получения отсортированного списка по частоте встречаемости
        Вторая, для сортировки при одинаковой частоте появления в лексикографическом порядке
        Функция возвращает отсорированный список
        """
        word_list = self.check_source_type()
        set_words = set(word_list)
        result = []
        for word in set_words:
            result.append((word_list.count(word), word))
        result.sort()
        result.sort(key=lambda x: x[0], reverse=True)
        return result

    def write_to_file(self) -> str:
        words = self.count_and_sort()
        with open("result_1.txt", "w+", encoding="UTF-8") as file:
            for word in words:
                file.write(f"{word[1]} {word[0]} \n")
        return "Finished!"

    def output_to_console(self) -> str:
        words = self.count_and_sort()
        for word in words:
            print(f"{word[1]} {word[0]}")
        return "Finished!"


if __name__ == '__main__':
    text = TextParser("resource_1.txt")
    # print(text.output_to_console())
    print(text.write_to_file())