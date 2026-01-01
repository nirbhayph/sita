from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QHBoxLayout
)
from PySide6.QtCore import Qt, QTimer

from services.wireless_setup import WirelessSetupController


class WirelessScreen(QWidget):
    def __init__(self, on_back):
        super().__init__()
        self.on_back = on_back
        self.controller = WirelessSetupController()

        self._setup_ui()
        self._connect_signals()
        self._start_polling()

    # ---------- UI ----------

    def _setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.title = QLabel("Wireless Setup")
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.instructions = QLabel(
            "On your phone:\n\n"
            "1. Open Settings → Developer Options\n"
            "2. Tap Wireless Debugging\n"
            "3. Tap “Pair device with pairing code”\n"
            "4. Enter the details below\n"
        )
        self.instructions.setWordWrap(True)

        self.ip_port_input = QLineEdit()
        self.ip_port_input.setPlaceholderText("Phone IP:Port")

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("6-digit pairing code")
        self.code_input.setMaxLength(6)
        self.code_input.setAlignment(Qt.AlignCenter)

        self.pair_button = QPushButton("Pair Device")

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.ip_port_input)
        input_layout.addWidget(self.code_input)
        input_layout.addWidget(self.pair_button)

        self.status_label = QLabel("Waiting for device to connect…")
        self.status_label.setStyleSheet("color: gray;")

        self.back_button = QPushButton("Back")

        self.layout.addWidget(self.title)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.instructions)
        self.layout.addSpacing(10)
        self.layout.addLayout(input_layout)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.status_label)
        self.layout.addStretch()
        self.layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

    # ---------- Signals ----------

    def _connect_signals(self):
        self.pair_button.clicked.connect(self._on_pair_clicked)
        self.back_button.clicked.connect(self.on_back)

    # ---------- Polling ----------

    def _start_polling(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_state)
        self.timer.start(2000)

    # ---------- Handlers ----------

    def _on_pair_clicked(self):
        ip_port = self.ip_port_input.text().strip()
        code = self.code_input.text().strip()

        if not ip_port or len(code) != 6:
            self._set_status("Enter IP:Port and 6-digit code", "red")
            return

        self._set_status("Pairing device…", "gray")

        success, message = self.controller.pair(ip_port, code)
        if success:
            self._set_status("Pairing successful. Waiting for device…", "green")
        else:
            self._set_status(f"Pairing failed:\n{message}", "red")

    def refresh_state(self):
        state = self.controller.poll()

        if state.error:
            self._set_status(state.error, "orange")
            return

        if state.device_connected:
            self._set_status(
                f"Device connected ({state.device_name}) ✅",
                "green"
            )
            self.timer.stop()
            return

        if state.waiting_for_connection:
            self._set_status("Waiting for device to connect…", "gray")

    # ---------- Helpers ----------

    def _set_status(self, text: str, color: str):
        self.status_label.setText(text)
        self.status_label.setStyleSheet(f"color: {color};")