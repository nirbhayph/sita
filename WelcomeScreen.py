from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton
)
from PySide6.QtCore import Qt

class WelcomeScreen(QWidget):
    def __init__(self, on_next, on_cancel):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel("Welcome to Device Host Setup")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px;")

        next_button = QPushButton("Next")
        cancel_button = QPushButton("Cancel")

        next_button.clicked.connect(on_next)
        cancel_button.clicked.connect(on_cancel)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(next_button)

        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()
        layout.addLayout(button_layout)