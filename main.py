import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout
)

class Installer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Device Host Setup")
        self.setFixedSize(500, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Welcome to Device Host Setup")
        layout.addWidget(self.label)

        btn_layout = QHBoxLayout()

        self.cancel_btn = QPushButton("Cancel")
        self.next_btn = QPushButton("Next")

        self.cancel_btn.clicked.connect(self.close)
        self.next_btn.clicked.connect(self.on_next)

        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.next_btn)

        layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def on_next(self):
        self.label.setText("Installing dependencies...")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Installer()
    window.show()
    sys.exit(app.exec())
