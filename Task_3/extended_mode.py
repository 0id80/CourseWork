from PyQt5.QtWidgets import QWidget, QLineEdit, QGridLayout, QLabel, QSizePolicy, QComboBox, QPushButton, QMessageBox
from PyQt5.Qt import QRegExpValidator, QRegExp, QFont
from PyQt5.QtCore import Qt
from extended_display import Display
from importlib import import_module

# М
# Sinh, Mod,  y√x, lg10
# гиперболический синус,
# вычислить остаток от деления одного числа на другое;
# y-ый корень числа x, где y обычно является положительным целым числом,
# десятичный логарифм


class ExtendedModeWindow(QWidget):
    _normal_size = 500, 650
    _default_id = 70151631
    _memory_cells = {}

    # ==========================================================================

    @staticmethod
    def _error_message_box(error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle('Calculate error')
        msg.setText('An exception occurred when calculating the result!')
        msg.setInformativeText(str(error))
        msg.exec_()

    @property
    def memory_cells_count(self):
        count = 0
        n = sum([int(char) for char in list(str(self._default_id)[-3:])])
        if len(str(n)) > 1:
            count = sum([int(char) for char in list(str(n)[-3:])])
        else:
            return n
        if count == 1:
            return 2
        else:
            return count

    def calculate_memory(self):
        count = self.memory_cells_count
        self._memory_cells.clear()
        for cell in range(count):
            self._memory_cells[f"Memory {cell + 1}"] = 0
        self.button_memory_change.clear()
        self.button_memory_change.addItems(self._memory_cells.keys())

    # ==========================================================================

    def display_cells_count(self):
        count = 0
        n = sum([int(char) for char in list(str(self._default_id))])
        if len(str(n)) > 1:
            count = sum([int(char) for char in list(str(n))])
        else:
            return n
        if count == 1:
            return 10
        else:
            return count

    def calculate_display_rows(self):
        count = self.display_cells_count()
        self.display.set_rows_count(count)

    def __init__(self):
        super(ExtendedModeWindow, self).__init__()
        self.grid_layout = QGridLayout()
        self.grid_layout.setObjectName("grid_layout")
        self.setWindowTitle("Calculator - Extended Mode")
        self.resize(*self._normal_size)
        self.setMinimumSize(*self._normal_size)
        self.setStyleSheet(u"QTextBrowser { border: 0px; font-size 25pt; }"
                           u"QWidget { background-color: #333333; color: white } "
                           u"QPushButton { color: black; font-size: 15pt; background-color: #f4f4f4 } "
                           u"QLineEdit { border: 0px; border-bottom: 1px solid white ; font-size: 15pt; }")

        self.label_bio = QLabel()
        self.label_bio.setText('Малых Евгений Александрович')
        self.label_bio.setFont(QFont("Calibri", 25))
        self.label_bio.setAlignment(Qt.AlignCenter)
        self.label_bio.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.grid_layout.addWidget(self.label_bio, 0, 0, 1, 5)

        self.label_id = QLabel()
        self.label_id.setText('MUIV ID:')
        self.label_id.setFont(QFont("Calibri", 15))
        self.label_id.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_id.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.grid_layout.addWidget(self.label_id, 1, 0, 1, 1)

        self.display_id = QLineEdit()
        self.display_id.setText(str(self._default_id))
        self.display_id.setFont(QFont("Calibri", 15))
        self.display_id.setAlignment(Qt.AlignCenter)
        self.display_id.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.display_id.setValidator(QRegExpValidator(QRegExp(r'\d{8}')))
        self.grid_layout.addWidget(self.display_id, 1, 1, 1, 1)

        self.display = Display()
        self.display.setFont(QFont("Calibri", 12))
        self.display.setFocusPolicy(Qt.NoFocus)
        self.display.setReadOnly(True)
        self.display.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.calculate_display_rows()
        self.grid_layout.addWidget(self.display, 2, 0, 1, 5)

        self.button_normal_mode = self.create_button("≡", position=(3, 0))
        self.button_calculate_display_memory = self.create_button("<>", position=(3, 1))

        self.button_memory_change = QComboBox()
        self.button_memory_change.setFont(QFont("Calibri", 14))
        self.button_memory_change.clear()
        self.button_memory_change.addItems(self._memory_cells.keys())
        self.grid_layout.addWidget(self.button_memory_change, 3, 2)

        self.button_deletion = self.create_button("←", position=(3, 3))
        self.button_clear = self.create_button("C", position=(3, 4))

        self.button_sinh = self.create_button("sinh", position=(4, 0))
        self.button_mod = self.create_button("mod", position=(4, 1))
        self.button_y_x = self.create_button("ʸ√ₓ", position=(4, 2))
        self.button_lg_10 = self.create_button("lg10", position=(4, 3))
        self.button_clear_all = self.create_button("CE", position=(4, 4))

        self.button_memory_clear = self.create_button("MC", position=(5, 0))
        self.button_memory_read = self.create_button("MR", position=(5, 1))
        self.button_memory_save = self.create_button("MS", position=(5, 2))
        self.button_memory_plus = self.create_button("M+", position=(5, 3))
        self.ext_button_memory_minus = self.create_button("M-", position=(5, 4))

        self.button_7 = self.create_button("7", position=(6, 0))
        self.button_8 = self.create_button("8", position=(6, 1))
        self.button_9 = self.create_button("9", position=(6, 2))
        self.button_division = self.create_button("/", position=(6, 3))
        self.button_degree = self.create_button("x^y", position=(6, 4))

        self.button_4 = self.create_button("4", position=(7, 0))
        self.button_5 = self.create_button("5", position=(7, 1))
        self.button_6 = self.create_button("6", position=(7, 2))
        self.button_multiplication = self.create_button("*", position=(7, 3))
        self.button_root = self.create_button("√", position=(7, 4))

        self.button_1 = self.create_button("1", position=(8, 0))
        self.button_2 = self.create_button("2", position=(8, 1))
        self.button_3 = self.create_button("3", position=(8, 2))
        self.button_minus = self.create_button("-", position=(8, 3))
        self.button_negative = self.create_button("±", position=(8, 4))

        self.button_0 = self.create_button("0", position=(9, 0, 1, 2))
        self.button_point = self.create_button(".", position=(9, 2))
        self.button_plus = self.create_button("+", position=(9, 3))
        self.button_equal = self.create_button("=", position=(9, 4))

        self.setLayout(self.grid_layout)

        self.calculate_memory()

    # ==========================================================================

    def add_to_display(self, button_data: str):
        def event(*_, extended_form: ExtendedModeWindow = self, button_value: str = button_data, **__):
            # print(button_value)
            simple_operation = ["/", "*", "-", "+"]

            if button_value == "≡":
                from normal_mode import NormalModeWindow
                extended_form.normal_mode = NormalModeWindow()
                extended_form.normal_mode.show()
                extended_form.close()

            elif button_value == "=":
                # DYNAMIC IMPORT ZONE -------------------------
                math = import_module('math')
                # WARNING
                # All these imports are used in the eval function
                log10 = getattr(math, 'log10')
                sinh = getattr(math, 'sinh')
                mod = getattr(math, 'fmod')
                # END OF DYNAMIC IMPORT ZONE ------------------

                if not (extended_form.display.prev_line == '' and extended_form.display.last_line == '0') and \
                        extended_form.display.prev_line[-1:] != '=':
                    if extended_form.display.prev_line == '':
                        expression = extended_form.display.last_line
                    elif extended_form.display.last_line == '':
                        if extended_form.display.prev_line[-1:] in simple_operation + ["^"]:
                            expression = extended_form.display.prev_line[:-1]
                        else:
                            expression = extended_form.display.prev_line
                    else:
                        if extended_form.display.last_line[:1] == '-':
                            expression = extended_form.display.prev_line + '(' + extended_form.display.last_line + ')'
                        else:
                            expression = extended_form.display.prev_line + extended_form.display.last_line
                    extended_form.display.prev_line = expression + '='
                    expression = expression.replace('×', '*').replace('÷', '/').replace('^', '**').replace('√', 'sqrt')
                    try:
                        extended_form.display.last_line = str(eval(expression))
                    except Exception as error:
                        extended_form._error_message_box(error)

            elif button_value.isdecimal():
                if extended_form.display.prev_line != "" and \
                        extended_form.display.prev_line[-1:] not in simple_operation + ["^"]:
                    extended_form.display.prev_line += "*"

                if extended_form.display.last_line == "0":
                    extended_form.display.last_line = button_value
                else:
                    extended_form.display.last_line = extended_form.display.last_line + button_value

            elif button_value == ".":
                if extended_form.display.last_line != "" and extended_form.display.last_line[-1:] != "." and \
                                                      "." not in extended_form.display.last_line:
                    extended_form.display.last_line = extended_form.display.last_line + button_value

            elif button_value in simple_operation:
                if extended_form.display.last_line != "":
                    if extended_form.display.last_line[-1:] == ")":
                        if button_value in simple_operation:
                            extended_form.display.prev_line = extended_form.display.prev_line + button_value
                        else:
                            extended_form.display.prev_line = extended_form.display.prev_line + "*" + \
                                                              extended_form.display.last_line
                    elif extended_form.display.prev_line[-1:] == "=":
                        extended_form.display.prev_line = extended_form.display.last_line + button_value
                        extended_form.display.last_line = "0"
                    else:
                        extended_form.display.prev_line = extended_form.display.prev_line + \
                                                          extended_form.display.last_line + button_value
                        extended_form.display.last_line = ""
                elif extended_form.display.prev_line[-1:] in simple_operation:
                    extended_form.display.prev_line = extended_form.display.prev_line[:-1] + button_value
                else:
                    extended_form.display.prev_line = extended_form.display.prev_line + button_value

            elif button_value == "<>":
                currect_id = extended_form.display_id.text()
                if currect_id != "":
                    self._default_id = currect_id
                    extended_form.calculate_memory()
                    extended_form.calculate_display_rows()
                else:
                    extended_form.display_id.setText(str(self._default_id))

            elif button_value == "←":
                if extended_form.display.last_line != "0":
                    extended_form.display.last_line = extended_form.display.last_line[:-1]
                if len(extended_form.display.last_line) == 0:
                    extended_form.display.last_line = "0"

            elif button_value == "C":
                extended_form.display.last_line = "0"

            elif button_value == "CE":
                extended_form.display.clear()

            # ==================================================================

            elif button_value == "MC":
                current_memory = self.button_memory_change.currentText()
                extended_form._memory_cells[current_memory] = 0
                pass

            elif button_value == "MR":
                if extended_form.display.prev_line != "" and \
                        extended_form.display.prev_line[-1:] not in simple_operation + ["^"]:
                    extended_form.display.prev_line += "*"

                current_memory = self.button_memory_change.currentText()
                extended_form.display.last_line = str(extended_form._memory_cells[current_memory])

            elif button_value == "MS":
                if extended_form.display.expression_result != "":
                    current_memory = self.button_memory_change.currentText()
                    extended_form._memory_cells[current_memory] = str(extended_form.display.expression_result)

            elif button_value == "M+":
                if extended_form.display.last_line != "":
                    current_memory = self.button_memory_change.currentText()
                    extended_form._memory_cells[current_memory] += extended_form.display.expression_result

            elif button_value == "M-":
                if extended_form.display.last_line != "":
                    current_memory = self.button_memory_change.currentText()
                    extended_form._memory_cells[current_memory] -= extended_form.display.expression_result

            # ==================================================================

            elif extended_form.display.last_line != "":

                if button_value == "sinh":
                    extended_form.display.prev_line = extended_form.display.prev_line + \
                                                          f"sinh({extended_form.display.last_line})"

                elif button_value == "mod":
                    if "X" in extended_form.display.prev_line:
                        extended_form.display.prev_line = extended_form.display.prev_line.replace("X", extended_form.display.last_line)
                    else:
                        extended_form.display.prev_line = extended_form.display.prev_line + \
                                                          f"mod({extended_form.display.last_line}, X)"

                elif button_value == "ʸ√ₓ":
                    if "Y" in extended_form.display.prev_line:
                        extended_form.display.prev_line = extended_form.display.prev_line.replace("Y", extended_form.display.last_line)
                    else:
                        extended_form.display.prev_line = extended_form.display.prev_line + \
                                                          f"({extended_form.display.last_line}^(1/Y))"

                elif button_value == "lg10":
                    extended_form.display.prev_line = extended_form.display.prev_line + \
                                                      f"log10({extended_form.display.last_line})"

                elif button_value == "x^y":
                    if "Y" in extended_form.display.prev_line:
                        extended_form.display.prev_line = extended_form.display.prev_line.replace("Y", extended_form.display.last_line)
                    else:
                        extended_form.display.prev_line = extended_form.display.prev_line + \
                                                          f"{extended_form.display.last_line}^Y"

                elif button_value == "√":
                    extended_form.display.prev_line = extended_form.display.prev_line + \
                                                      f"({extended_form.display.last_line}^(1/2))"

                elif button_value == "±":
                    extended_form.display.prev_line = extended_form.display.prev_line + \
                                                      f"(-{extended_form.display.last_line})"
                extended_form.display.last_line = ""

            # ==================================================================

        return event

    def create_button(self, text: str, position: tuple) -> QPushButton:
        button = QPushButton()
        button.setText(text)
        button.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        button.clicked.connect(self.add_to_display(text))
        self.grid_layout.addWidget(button, *position)
        return button
