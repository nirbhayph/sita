from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QProgressBar, QTextEdit
)
from PySide6.QtCore import Slot

from services.installers.install_worker import InstallWorker


class InstallerPage(QWidget):

    def __init__(self, on_next=None, on_back=None):
        super().__init__()
        self.on_next = on_next
        self.on_back = on_back
        self.worker = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.status = QLabel("Click Install to begin")
        self.progress = QProgressBar()
        self.log = QTextEdit(readOnly=True)

        self.install_btn = QPushButton("Install")
        self.next_btn = QPushButton("Next")
        self.back_btn = QPushButton("Back")

        self.next_btn.setEnabled(False)

        self.install_btn.clicked.connect(self.start_install)
        self.next_btn.clicked.connect(lambda: self.on_next and self.on_next())
        self.back_btn.clicked.connect(lambda: self.on_back and self.on_back())

        btns = QHBoxLayout()
        btns.addWidget(self.back_btn)
        btns.addStretch()
        btns.addWidget(self.install_btn)
        btns.addWidget(self.next_btn)

        layout.addWidget(self.status)
        layout.addWidget(self.progress)
        layout.addWidget(self.log)
        layout.addLayout(btns)

    def start_install(self):
        self.install_btn.setEnabled(False)
        self.back_btn.setEnabled(False)  # 🔒 disable during install

        self.worker = InstallWorker()
        self.worker.progress.connect(self.progress.setValue)
        self.worker.status.connect(self.log.append)
        self.worker.finished.connect(self.finish_install)
        self.worker.start()

    @Slot(bool, str)
    def finish_install(self, success, message):
        self.log.append(message)

        if success:
            self.status.setText("Installation completed successfully")
            self.next_btn.setEnabled(True)
            self.install_btn.setEnabled(False)
        else:
            self.status.setText("Installation failed")
            self.install_btn.setEnabled(True)
            self.back_btn.setEnabled(True)  # ✅ restore back

