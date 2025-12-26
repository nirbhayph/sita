from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QHBoxLayout
)
from PySide6.QtCore import Qt, QTimer
import subprocess


class WirelessScreen(QWidget):
    def __init__(self, on_back):
        super().__init__()
        self.device_connected = False
        self.waiting_for_connection = False

        layout = QVBoxLayout(self)

        # -------------------------
        # Title
        # -------------------------
        title = QLabel("Wireless Setup")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        # -------------------------
        # Instructions
        # -------------------------
        instructions = QLabel(
            "On your phone:\n\n"
            "1. Open Settings → Developer Options\n"
            "2. Tap Wireless Debugging\n"
            "3. Tap “Pair device with pairing code”\n"
            "4. Enter the details below\n"
        )
        instructions.setWordWrap(True)

        # -------------------------
        # Inputs
        # -------------------------
        self.ip_port_input = QLineEdit()
        self.ip_port_input.setPlaceholderText(
            "Phone IP:Port (example: 192.168.1.42:37173)"
        )

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("6-digit pairing code")
        self.code_input.setMaxLength(6)
        self.code_input.setAlignment(Qt.AlignCenter)

        pair_button = QPushButton("Pair Device")
        pair_button.clicked.connect(self.pair_device)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.ip_port_input)
        input_layout.addWidget(self.code_input)
        input_layout.addWidget(pair_button)

        # -------------------------
        # Status
        # -------------------------
        self.status_label = QLabel("Waiting for device to connect…")
        self.status_label.setStyleSheet("color: gray;")

        # -------------------------
        # Navigation
        # -------------------------
        back_button = QPushButton("Back")
        back_button.clicked.connect(on_back)

        # -------------------------
        # Layout
        # -------------------------
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(instructions)
        layout.addSpacing(10)
        layout.addLayout(input_layout)
        layout.addSpacing(10)
        layout.addWidget(self.status_label)
        layout.addStretch()
        layout.addWidget(back_button, alignment=Qt.AlignLeft)

        # -------------------------
        # Poll ADB
        # -------------------------
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_wireless_connection)
        self.timer.start(2000)

        self.check_wireless_connection()

    # -------------------------
    # Pairing
    # -------------------------
    def pair_device(self):
        ip_port = self.ip_port_input.text().strip()
        code = self.code_input.text().strip()

        if not ip_port or len(code) != 6:
            self.status_label.setText("Enter IP:Port and 6-digit code")
            self.status_label.setStyleSheet("color: red;")
            return

        try:
            self.status_label.setText("Pairing device…")
            self.status_label.setStyleSheet("color: gray;")

            proc = subprocess.Popen(
                ["adb", "pair", ip_port],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = proc.communicate(code + "\n", timeout=15)

            if proc.returncode == 0:
                self.waiting_for_connection = True  # 🔒 lock state
                self.status_label.setText("Pairing successful. Waiting for device…")
                self.status_label.setStyleSheet("color: green;")

            else:
                self.status_label.setText(
                    "Pairing failed:\n" + (stderr.strip() or stdout.strip())
                )
                self.status_label.setStyleSheet("color: red;")

        except Exception as e:
            self.status_label.setText(f"ADB error: {e}")
            self.status_label.setStyleSheet("color: red;")

    # -------------------------
    # Connection detection
    # -------------------------
    def check_wireless_connection(self):
        if self.device_connected:
            return

        try:
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True,
                text=True
            )

            for line in result.stdout.splitlines()[1:]:
                line = line.strip()

                # Wireless devices have ip:port
                if ":" in line:
                    device_id, status = line.split("\t", 1)

                    if status == "device":
                        device_name = self.get_device_name(device_id)

                        self.status_label.setText(
                            f"Device connected ({device_name}) ✅"
                        )
                        self.status_label.setStyleSheet("color: green;")

                        self.device_connected = True
                        self.waiting_for_connection = False
                        self.timer.stop()
                        return

                    elif status == "unauthorized":
                        self.status_label.setText(
                            "Device connected but not authorized. Check phone."
                        )
                        self.status_label.setStyleSheet("color: orange;")
                        return

            if not self.waiting_for_connection:
                self.status_label.setText("Waiting for device to connect…")
                self.status_label.setStyleSheet("color: gray;")

        except Exception:
            self.status_label.setText("ADB not available")
            self.status_label.setStyleSheet("color: red;")

    # -------------------------
    # Device name
    # -------------------------
    def get_device_name(self, device_id):
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "shell", "getprop", "ro.product.model"],
                capture_output=True,
                text=True,
                timeout=2
            )

            name = result.stdout.strip()
            return name if name else "Android device"

        except Exception:
            return "Android device"
