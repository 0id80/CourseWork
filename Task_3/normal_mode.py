from PyQt5 import QtWidgets, QtCore, Qt


class NormalModeWindow(QtWidgets.QWidget):
    _normal_size = 350, 550
    _memory_cell = 0

    def __init__(self):
        super(NormalModeWindow, self).__init__()
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setObjectName("grid_layout")
        self.setWindowTitle("Calculator - Normal Mode")
        self.resize(*self._normal_size)
        self.setMinimumSize(*self._normal_size)
        self.setStyleSheet(u"QWidget { background-color: #333333; color: white } "
                           u"QPushButton { color: black; font-size: 15pt; background-color: #f4f4f4 } "
                           u"QLineEdit { border: 0px solid white; font-size: 15pt; }")

        self.display_label = QtWidgets.QLineEdit()
        self.display_label.setText("0")
        self.display_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.display_label.setDragEnabled(False)
        self.display_label.setReadOnly(True)
        self.display_label.setAlignment(Qt.Qt.AlignRight)
        self.display_label.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                                   QtWidgets.QSizePolicy.Minimum))

        self.display_memory = QtWidgets.QLineEdit()
        self.display_memory.setText("")
        self.display_memory.setFocusPolicy(QtCore.Qt.NoFocus)
        self.display_memory.setDragEnabled(False)
        self.display_memory.setReadOnly(True)
        self.display_memory.setAlignment(Qt.Qt.AlignRight)
        self.display_memory.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                                   QtWidgets.QSizePolicy.Minimum))

        self.grid_layout.addWidget(self.display_memory, 1, 1, 1, 5)

        self.grid_layout.addWidget(self.display_label, 2, 2, 1, 3)

        self.button_extended_mode = self.create_button("≡", position=(2, 1))
        self.button_clear = self.create_button("C", position=(2, 5))

        self.button_memory_clear = self.create_button("MC", position=(3, 1))
        self.button_memory_read = self.create_button("MR", position=(3, 2))
        self.button_memory_save = self.create_button("MS", position=(3, 3))
        self.button_memory_plus = self.create_button("M+", position=(3, 4))
        self.button_memory_minus = self.create_button("M-", position=(3, 5))

        self.button_7 = self.create_button("7", position=(4, 1))
        self.button_8 = self.create_button("8", position=(4, 2))
        self.button_9 = self.create_button("9", position=(4, 3))
        self.button_division = self.create_button("/", position=(4, 4))
        self.button_degree = self.create_button("x^y", position=(4, 5))

        self.button_4 = self.create_button("4", position=(5, 1))
        self.button_5 = self.create_button("5", position=(5, 2))
        self.button_6 = self.create_button("6", position=(5, 3))
        self.button_multiplication = self.create_button("*", position=(5, 4))
        self.button_root = self.create_button("√", position=(5, 5))

        self.button_1 = self.create_button("1", position=(6, 1))
        self.button_2 = self.create_button("2", position=(6, 2))
        self.button_3 = self.create_button("3", position=(6, 3))
        self.button_minus = self.create_button("-", position=(6, 4))
        self.button_negative = self.create_button("±", position=(6, 5))

        self.button_0 = self.create_button("0", position=(7, 1, 1, 2))
        self.button_point = self.create_button(".", position=(7, 3))
        self.button_plus = self.create_button("+", position=(7, 4))
        self.button_equal = self.create_button("=", position=(7, 5))

        self.setLayout(self.grid_layout)

    def add_to_display(self, button_data: str):
        def event(*_, normal_form: NormalModeWindow = self, button_value: str = button_data, **__):
            simple_operation = ["/", "*", "-", "+"]

            display_memory = normal_form.display_memory.text()
            current_display = normal_form.display_label.text()

            if button_value == "≡":
                from extended_mode import ExtendedModeWindow
                normal_form.extended_mode = ExtendedModeWindow()
                normal_form.extended_mode.show()
                normal_form.close()
            elif button_value == "C":
                normal_form.display_memory.setText("")
                normal_form.display_label.setText("0")

            elif button_value == "MC":
                normal_form._memory_cell = 0
            elif button_value == "MR":
                normal_form.display_label.setText(str(normal_form._memory_cell))
            elif button_value == "MS":
                normal_form._memory_cell = float(current_display)
            elif button_value == "M+":
                normal_form._memory_cell += float(current_display)
            elif button_value == "M-":
                normal_form._memory_cell -= float(current_display)

            elif button_value.isdecimal():
                if len(display_memory) > 1 and display_memory[-1] == "=":
                    normal_form.display_label.setText(str(button_value))
                    normal_form.display_memory.setText("")
                else:
                    if current_display != "0":
                        normal_form.display_label.setText(current_display + button_value)
                    else:
                        normal_form.display_label.setText(button_value)

            elif button_value in simple_operation:
                if current_display != "":
                    if display_memory[-1:] == ")":
                        if button_value in simple_operation:
                            normal_form.display_memory.setText(display_memory + button_value)
                        else:
                            normal_form.display_memory.setText(display_memory + "*" + current_display)
                    elif display_memory[-1:] == "=":
                        normal_form.display_memory.setText(current_display + button_value)
                        normal_form.display_label.setText("0")
                    else:
                        normal_form.display_memory.setText(display_memory + current_display + button_value)
                        normal_form.display_label.setText("")
                elif display_memory[-1:] in simple_operation:
                    normal_form.display_memory.setText(display_memory[:-1] + button_value)
                else:
                    normal_form.display_memory.setText(display_memory + button_value)

            elif button_value == "x^y":
                if display_memory == "":
                    normal_form.display_memory.setText(current_display + "^")
                elif display_memory[-1] == "^":
                    normal_form.display_memory.setText(display_memory + current_display)
                elif display_memory[-1] == ")":
                    normal_form.display_memory.setText(display_memory + "^" + current_display)
                normal_form.display_label.setText("0")

            elif button_value == "√":
                if len(display_memory) > 1:
                    if display_memory[-1] in simple_operation:
                        normal_form.display_memory.setText(display_memory + f"({current_display}^(1/2))")
                    else:
                        normal_form.display_memory.setText(display_memory + "*" + f"({current_display}^(1/2))")
                else:
                    normal_form.display_memory.setText(f"({current_display}^(1/2))")
                normal_form.display_label.setText("0")

            elif button_value == "±":
                normal_form.display_memory.setText(display_memory + f"(-{current_display})")
                normal_form.display_label.setText("0")

            elif button_value == ".":
                if current_display != "" and current_display[-1:] != "." and "." not in current_display:
                    normal_form.display_label.setText(current_display + button_value)

            elif button_value == "=":
                if display_memory != "":
                    if current_display != "":
                        if display_memory[-1] == ")":
                            normal_form.display_memory.setText(f"{normal_form.display_memory.text().replace('^', '**')}=")
                        else:
                            normal_form.display_memory.setText(f"{normal_form.display_memory.text().replace('^', '**')}{current_display}=")
                    else:
                        normal_form.display_memory.setText(f"{normal_form.display_memory.text()[:-1].replace('^', '**')}=")
                    normal_form.display_label.setText(str(eval(normal_form.display_memory.text()[:-1])))
        return event

    def create_button(self, text: str, position: tuple) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton()
        button.setText(text)
        button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                                   QtWidgets.QSizePolicy.Minimum))
        button.clicked.connect(self.add_to_display(text))
        self.grid_layout.addWidget(button, *position)
        return button
