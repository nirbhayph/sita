from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton
)
from PySide6.QtCore import Qt


class WelcomeScreen(QWidget):
    TITLE_TEXT = "Welcome to Device Host Setup"

    def __init__(self, on_next, on_cancel):
        super().__init__()
        self.on_next = on_next
        self.on_cancel = on_cancel

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.title_label = QLabel(self.TITLE_TEXT)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px;")

        self.next_button = QPushButton("Next")
        self.cancel_button = QPushButton("Cancel")

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.next_button)

        self.layout.addStretch()
        self.layout.addWidget(self.title_label)
        self.layout.addStretch()
        self.layout.addLayout(self.button_layout)

    def _connect_signals(self):
        self.next_button.clicked.connect(self.on_next)
        self.cancel_button.clicked.connect(self.on_cancel)
