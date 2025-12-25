from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout
)
from PySide6.QtCore import QTimer
import subprocess


def _noop():
    pass


class WiredScreen(QWidget):
    def __init__(self, on_back, on_next=None):
        super().__init__()

        if on_next is None:
            on_next = _noop

        layout = QVBoxLayout(self)

        title = QLabel("Wired Setup")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        info = QLabel("• Connect your phone using USB")

        self.device_status_label = QLabel("Device: Not connected")
        self.device_status_label.setStyleSheet("color: gray;")

        self.debug_status_label = QLabel("USB Debugging: Disabled")
        self.debug_status_label.setStyleSheet("color: gray;")

        self.next_button = QPushButton("Next")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(on_next)

        back_button = QPushButton("Back")
        back_button.clicked.connect(on_back)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(back_button)
        btn_layout.addStretch()
        btn_layout.addWidget(self.next_button)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(info)
        layout.addSpacing(10)
        layout.addWidget(self.device_status_label)
        layout.addWidget(self.debug_status_label)
        layout.addStretch()
        layout.addLayout(btn_layout)

        # Poll USB state
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_state)
        self.timer.start(2000)

        self.refresh_state()

    def refresh_state(self):
        device_id = self.get_connected_device_id()

        if not device_id:
            self.device_status_label.setText("Device: Not connected")
            self.device_status_label.setStyleSheet("color: gray;")

            self.debug_status_label.setText("USB Debugging: Disabled")
            self.debug_status_label.setStyleSheet("color: gray;")

            self.next_button.setEnabled(False)
            return

        # Device connected
        model = self.get_device_model(device_id)
        self.device_status_label.setText(f"Device: Connected ({model})")
        self.device_status_label.setStyleSheet("color: green;")

        # Check USB debugging
        if self.is_usb_debugging_enabled(device_id):
            self.debug_status_label.setText("USB Debugging: Enabled")
            self.debug_status_label.setStyleSheet("color: green;")
            self.next_button.setEnabled(True)
        else:
            self.debug_status_label.setText("USB Debugging: Disabled")
            self.debug_status_label.setStyleSheet("color: red;")
            self.next_button.setEnabled(False)

    def get_connected_device_id(self):
        try:
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True,
                text=True
            )

            for line in result.stdout.splitlines()[1:]:
                if "\tdevice" in line:
                    return line.split("\t")[0]

            return None
        except Exception:
            return None

    def get_device_model(self, device_id):
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "shell", "getprop", "ro.product.model"],
                capture_output=True,
                text=True,
                timeout=2
            )
            return result.stdout.strip() or "Unknown device"
        except Exception:
            return "Unknown device"

    def is_usb_debugging_enabled(self, device_id):
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "shell", "echo", "ok"],
                capture_output=True,
                text=True,
                timeout=2
            )
            return result.stdout.strip() == "ok"
        except Exception:
            return False
