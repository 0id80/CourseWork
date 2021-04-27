from PyQt5.QtWidgets import QTextBrowser
from PyQt5.Qt import Qt


class Display(QTextBrowser):
    _default_text = "\n0"

    def __init__(self, parent=None):
        super(Display, self).__init__(parent)
        self.clear()

    def clear(self, text=_default_text):
        super(Display, self).clear()
        self.setText(text)

    def setText(self, text: str) -> None:
        super(Display, self).setText(text)
        self.selectAll()
        self.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)

    @property
    def __rows(self):
        return self.toPlainText().split("\n")

    @property
    def expression_result(self):
        return self.__rows[-1]

    @property
    def prev_line(self):
        if self.__rows[-2].endswith("="):
            self.append(self._default_text)
        return self.__rows[-2]

    @prev_line.setter
    def prev_line(self, value):
        strings = self.__rows[:-2]
        strings.append(value)
        strings.append(self.__rows[-1])
        self.setText("\n".join(strings))

    @property
    def last_line(self):
        if self.__rows[-2].endswith("="):
            self.append(self._default_text)
        return self.expression_result

    @last_line.setter
    def last_line(self, value):
        strings = self.__rows[:-1]
        strings.append(value)
        self.setText("\n".join(strings))

    def set_rows_count(self, count):
        self.setFixedHeight(self.fontMetrics().height() * count)
