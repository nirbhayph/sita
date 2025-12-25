from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton
)
from PySide6.QtCore import Qt

class FinishScreen(QWidget):
    def __init__(self, on_next, on_back):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel("Thank you for accepting the Terms & Conditions.")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px;")

        back_button = QPushButton("Back")
        next_button = QPushButton("Next")

        back_button.clicked.connect(on_back)
        next_button.clicked.connect(on_next)

        button_layout = QHBoxLayout()
        button_layout.addWidget(back_button)
        button_layout.addStretch()
        button_layout.addWidget(next_button)

        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()
        layout.addLayout(button_layout)