from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QRadioButton,
    QButtonGroup,
    QPushButton,
    QHBoxLayout
)

terms_text = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus.
Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor.
Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi.
Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat.
""" * 10


class TermsScreen(QWidget):
    def __init__(self, on_accept, on_back):
        super().__init__()

        self.on_accept = on_accept
        self.on_back = on_back

        layout = QVBoxLayout(self)

        title = QLabel("Terms and Conditions")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        terms_box = QTextEdit()
        terms_box.setReadOnly(True)
        terms_box.setText(terms_text)

        agree_radio = QRadioButton("I Agree")
        disagree_radio = QRadioButton("I Disagree")

        radio_group = QButtonGroup(self)
        radio_group.addButton(agree_radio)
        radio_group.addButton(disagree_radio)

        next_button = QPushButton("Next")
        back_button = QPushButton("Back")
        next_button.setEnabled(False)

        agree_radio.toggled.connect(
            lambda checked: next_button.setEnabled(checked)
        )

        next_button.clicked.connect(self.on_accept)
        back_button.clicked.connect(self.on_back)

        radio_layout = QVBoxLayout()
        radio_layout.addWidget(agree_radio)
        radio_layout.addWidget(disagree_radio)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(back_button)
        btn_layout.addWidget(next_button)

        layout.addWidget(title)
        layout.addWidget(terms_box)
        layout.addLayout(radio_layout)
        layout.addLayout(btn_layout)
