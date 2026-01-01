from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout
)
from PySide6.QtCore import QTimer

from services.wired_setup import WiredSetupController


def _noop():
    pass


class WiredScreen(QWidget):
    def __init__(self, on_back, on_next=None):
        super().__init__()

        self.on_back = on_back
        self.on_next = on_next or _noop

        self.controller = WiredSetupController()

        self._setup_ui()
        self._connect_signals()
        self._start_polling()

        self.refresh_state()

    # ---------- UI ----------

    def _setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.title = QLabel("Wired Setup")
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.info = QLabel("• Connect your phone using USB")

        self.device_status_label = QLabel("Device: Not connected")
        self.debug_status_label = QLabel("USB Debugging: Disabled")

        self.next_button = QPushButton("Next")
        self.next_button.setEnabled(False)

        self.back_button = QPushButton("Back")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.back_button)
        btn_layout.addStretch()
        btn_layout.addWidget(self.next_button)

        self.layout.addWidget(self.title)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.info)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.device_status_label)
        self.layout.addWidget(self.debug_status_label)
        self.layout.addStretch()
        self.layout.addLayout(btn_layout)

    # ---------- Signals ----------

    def _connect_signals(self):
        self.back_button.clicked.connect(self.on_back)
        self.next_button.clicked.connect(self.on_next)

    # ---------- Polling ----------

    def _start_polling(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_state)
        self.timer.start(2000)

    # ---------- State ----------

    def refresh_state(self):
        state = self.controller.get_state()

        if not state.device_connected:
            self._set_disconnected_ui()
            return

        self._set_connected_ui(state)

    def _set_disconnected_ui(self):
        self.device_status_label.setText("Device: Not connected")
        self.device_status_label.setStyleSheet("color: gray;")

        self.debug_status_label.setText("USB Debugging: Disabled")
        self.debug_status_label.setStyleSheet("color: gray;")

        self.next_button.setEnabled(False)

    def _set_connected_ui(self, state):
        self.device_status_label.setText(
            f"Device: Connected ({state.device_model})"
        )
        self.device_status_label.setStyleSheet("color: green;")

        if state.usb_debugging_enabled:
            self.debug_status_label.setText("USB Debugging: Enabled")
            self.debug_status_label.setStyleSheet("color: green;")
            self.next_button.setEnabled(True)
        else:
            self.debug_status_label.setText("USB Debugging: Disabled")
            self.debug_status_label.setStyleSheet("color: red;")
            self.next_button.setEnabled(False)
