from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton
)
from PySide6.QtCore import Qt

class WelcomeScreen(QWidget):
    def __init__(self, on_next, on_cancel):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel("Welcome to Device Host Setup")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px;")

        next_btn = QPushButton("Next")
        cancel_btn = QPushButton("Cancel")

        next_btn.clicked.connect(on_next)
        cancel_btn.clicked.connect(on_cancel)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(next_btn)

        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()
        layout.addLayout(btn_layout)