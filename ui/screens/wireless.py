from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap

from services.device_setup.wireless_setup import WirelessSetupController


class WirelessScreen(QWidget):
    def __init__(self, on_back):
        super().__init__()
        self.on_back = on_back
        self.controller = WirelessSetupController()
        self.timer = None

        self._setup_ui()
        self._connect_signals()
        self._start_polling()

    # ---------- UI ----------

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.title = QLabel("Wireless Setup")
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.instructions = QLabel(
            "On your phone:\n\n"
            "1. Open Settings → Developer Options\n"
            "2. Tap Wireless Debugging\n"
            "3. Tap “Pair device with QR code”\n"
            "4. Scan the QR code shown below\n"
        )
        self.instructions.setWordWrap(True)

        # QR display
        self.qr_label = QLabel("QR code not generated")
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setMinimumHeight(240)
        self.qr_label.setStyleSheet("border: 1px dashed #aaa;")

        self.generate_qr_button = QPushButton("Generate QR Code")

        self.status_label = QLabel("Waiting to start pairing…")
        self.status_label.setStyleSheet("color: gray;")

        self.back_button = QPushButton("Back")

        layout.addWidget(self.title)
        layout.addSpacing(10)
        layout.addWidget(self.instructions)
        layout.addSpacing(10)
        layout.addWidget(self.qr_label)
        layout.addSpacing(10)
        layout.addWidget(self.generate_qr_button, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.status_label)
        layout.addStretch()
        layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

    # ---------- Signals ----------

    def _connect_signals(self):
        self.generate_qr_button.clicked.connect(self._on_generate_qr)
        self.back_button.clicked.connect(self._on_back_clicked)

    # ---------- Polling ----------

    def _start_polling(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._poll_pairing_state)
        self.timer.start(2000)

    # ---------- Handlers ----------

    def _on_generate_qr(self):
        try:
            self._set_status("Generating QR code…", "gray")

            qr_data = self.controller.start_qr_pairing()

            pixmap = QPixmap(qr_data.image_path)
            self.qr_label.setPixmap(
                pixmap.scaled(
                    220,
                    220,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

            self._set_status("Scan QR code on your phone", "green")

        except Exception as e:
            self._set_status(str(e), "red")

    def _poll_pairing_state(self):
        connected, model = self.controller.poll_for_device()

        if connected:
            self._set_status(
                f"Device connected successfully ✅\nModel: {model}",
                "green"
            )
            self.timer.stop()

    def _on_back_clicked(self):
        self._reset()
        self.on_back()

    # ---------- Reset ----------

    def _reset(self):
        # Stop polling
        if self.timer and self.timer.isActive():
            self.timer.stop()

        # Reset controller state
        self.controller = WirelessSetupController()

        # Reset UI
        self.qr_label.setText("QR code not generated")
        self.qr_label.setPixmap(QPixmap())

        self.status_label.setText("Waiting to start pairing…")
        self.status_label.setStyleSheet("color: gray;")

        # Restart polling
        self.timer.start(2000)

    # ---------- Helpers ----------

    def _set_status(self, text: str, color: str):
        self.status_label.setText(text)
        self.status_label.setStyleSheet(f"color: {color};")
