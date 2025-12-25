from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class WirelessScreen(QWidget):
    def __init__(self, on_back):
        super().__init__()
        layout = QVBoxLayout(self)

        title = QLabel("Wireless Setup")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        info1 = QLabel("• Enable wireless debugging")
        info2 = QLabel("• Laptop and Phone should be on the same network")

        image_label = QLabel()
        pixmap = QPixmap("Qr.png")
        image_label.setPixmap(pixmap.scaledToWidth(400, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)

        back_button = QPushButton("Back")
        back_button.clicked.connect(on_back)

        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(info1)
        layout.addWidget(info2)
        layout.addSpacing(20)
        layout.addWidget(image_label)
        layout.addStretch()
        layout.addWidget(back_button, alignment=Qt.AlignLeft)