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
from PySide6.QtCore import Qt


TERMS_TEXT = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus.
Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor.
Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi.
Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat.
""" * 10


class TermsScreen(QWidget):
    TITLE_TEXT = "Terms and Conditions"

    def __init__(self, on_accept, on_back):
        super().__init__()
        self.on_accept = on_accept
        self.on_back = on_back

        self._setup_ui()
        self._connect_signals()
        self._set_initial_state()

    # ---------- UI ----------

    def _setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.title_label = QLabel(self.TITLE_TEXT)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.terms_box = QTextEdit()
        self.terms_box.setReadOnly(True)
        self.terms_box.setText(TERMS_TEXT)

        self.agree_radio = QRadioButton("I Agree")
        self.disagree_radio = QRadioButton("I Disagree")

        self.radio_group = QButtonGroup(self)
        self.radio_group.addButton(self.agree_radio)
        self.radio_group.addButton(self.disagree_radio)

        self.next_button = QPushButton("Next")
        self.back_button = QPushButton("Back")

        self.radio_layout = QVBoxLayout()
        self.radio_layout.addWidget(self.agree_radio)
        self.radio_layout.addWidget(self.disagree_radio)

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.back_button)
        self.button_layout.addWidget(self.next_button)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.terms_box)
        self.layout.addLayout(self.radio_layout)
        self.layout.addLayout(self.button_layout)

    # ---------- State ----------

    def _set_initial_state(self):
        self.disagree_radio.setChecked(True)
        self.next_button.setEnabled(False)

    # ---------- Signals ----------

    def _connect_signals(self):
        self.agree_radio.toggled.connect(self._on_agree_toggled)
        self.next_button.clicked.connect(self.on_accept)
        self.back_button.clicked.connect(self.on_back)

    # ---------- Handlers ----------

    def _on_agree_toggled(self, checked: bool):
        self.next_button.setEnabled(checked)
