from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)
from PySide6.QtCore import Qt

class ConnectionSelectionScreen(QWidget):
    def __init__(self, on_wireless, on_wired, on_back):
        super().__init__()
        layout = QVBoxLayout(self)

        label = QLabel("How do you want to connect your device?")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px;")

        wireless_button = QPushButton("Wireless")
        wired_button = QPushButton("Wired (USB)")

        wireless_button.clicked.connect(on_wireless)
        wired_button.clicked.connect(on_wired)

        back_button = QPushButton("Back")
        back_button.clicked.connect(on_back)

        layout.addStretch()
        layout.addWidget(label)
        layout.addSpacing(20)
        layout.addWidget(wireless_button, alignment=Qt.AlignCenter)
        layout.addWidget(wired_button, alignment=Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(back_button, alignment=Qt.AlignLeft)