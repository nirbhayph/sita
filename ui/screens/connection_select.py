from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QListWidget,
    QGroupBox
)
from PySide6.QtCore import Qt, QTimer

from services.device_setup.device_discovery import DeviceDiscoveryService


class ConnectionSelectionScreen(QWidget):
    TITLE_TEXT = "How do you want to connect your device?"

    def __init__(self, on_wireless, on_wired, on_back):
        super().__init__()
        self.on_wireless = on_wireless
        self.on_wired = on_wired
        self.on_back = on_back

        self._setup_ui()
        self._connect_signals()
        self._start_polling()

    # ---------- UI ----------

    def _setup_ui(self):
        root = QVBoxLayout(self)

        # --- Device lists ---
        device_row = QHBoxLayout()

        self.wireless_list = QListWidget()
        self.wired_list = QListWidget()

        device_row.addWidget(self._wrap("Wireless devices", self.wireless_list))
        device_row.addWidget(self._wrap("Wired devices", self.wired_list))

        # --- Center section ---
        self.title_label = QLabel(self.TITLE_TEXT)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px;")

        self.wireless_button = QPushButton("Wireless")
        self.wired_button = QPushButton("Wired (USB)")
        self.back_button = QPushButton("Back")

        button_row = QHBoxLayout()
        button_row.addWidget(self.wireless_button)
        button_row.addWidget(self.wired_button)
        button_row.setAlignment(Qt.AlignCenter)

        # --- Assemble ---
        root.addLayout(device_row)
        root.addSpacing(20)
        root.addWidget(self.title_label)
        root.addSpacing(10)
        root.addLayout(button_row)
        root.addStretch()
        root.addWidget(self.back_button, alignment=Qt.AlignLeft)

    def _wrap(self, title: str, widget: QWidget) -> QGroupBox:
        box = QGroupBox(title)
        layout = QVBoxLayout(box)
        layout.addWidget(widget)
        return box

    # ---------- Signals ----------

    def _connect_signals(self):
        self.wireless_button.clicked.connect(self.on_wireless)
        self.wired_button.clicked.connect(self.on_wired)
        self.back_button.clicked.connect(self.on_back)

    # ---------- Polling ----------

    def _start_polling(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._refresh_devices)
        self.timer.start(2000)
        self._refresh_devices()

    def _refresh_devices(self):
        self.wireless_list.clear()
        self.wired_list.clear()

        for device in DeviceDiscoveryService.get_wireless_devices():
            self.wireless_list.addItem(device)

        for device in DeviceDiscoveryService.get_wired_devices():
            self.wired_list.addItem(device)
