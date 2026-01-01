from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)
from PySide6.QtCore import Qt


class ConnectionSelectionScreen(QWidget):
    TITLE_TEXT = "How do you want to connect your device?"

    def __init__(self, on_wireless, on_wired, on_back):
        super().__init__()
        self.on_wireless = on_wireless
        self.on_wired = on_wired
        self.on_back = on_back

        self._setup_ui()
        self._connect_signals()

    # ---------- UI ----------

    def _setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.title_label = QLabel(self.TITLE_TEXT)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px;")

        self.wireless_button = QPushButton("Wireless")
        self.wired_button = QPushButton("Wired (USB)")
        self.back_button = QPushButton("Back")

        self.layout.addStretch()
        self.layout.addWidget(self.title_label)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.wireless_button, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.wired_button, alignment=Qt.AlignCenter)
        self.layout.addStretch()
        self.layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

    # ---------- Signals ----------

    def _connect_signals(self):
        self.wireless_button.clicked.connect(self.on_wireless)
        self.wired_button.clicked.connect(self.on_wired)
        self.back_button.clicked.connect(self.on_back)
