from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)
from PySide6.QtCore import Qt

class FinishScreen(QWidget):
    def __init__(self, on_back):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel("Thank you for accepting the Terms & Conditions.")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px;")

        back_button = QPushButton("Back")
        back_button.clicked.connect(on_back)

        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(back_button, alignment=Qt.AlignCenter)