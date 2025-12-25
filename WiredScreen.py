from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)
from PySide6.QtCore import Qt

class WiredScreen(QWidget):
    def __init__(self, on_back):
        super().__init__()
        layout = QVBoxLayout(self)

        title = QLabel("Wired Setup")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        info = QLabel("• Enable USB debugging")

        back_button = QPushButton("Back")
        back_button.clicked.connect(on_back)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(info)
        layout.addStretch()
        layout.addWidget(back_button, alignment=Qt.AlignLeft)