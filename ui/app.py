from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget

from navigation.router import Router

from ui.screens.welcome import WelcomeScreen
from ui.screens.terms import TermsScreen
from ui.screens.installers import InstallerPage
#from InstallDependencies import InstallerPage
from ui.screens.connection_select import ConnectionSelectionScreen
from ui.screens.wireless import WirelessScreen
from ui.screens.wired import WiredScreen


class InstallerApp(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._setup_navigation()
        self._setup_layout()

        self.router.go("welcome")

    def _setup_window(self):
        self.setWindowTitle("Device Host Setup")
        self.setFixedSize(1000, 600)

    def _setup_navigation(self):
        self.stack = QStackedWidget(self)
        self.router = Router(self.stack)
        self._register_screens()

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

    def _register_screens(self):
        self.router.register(
            "welcome",
            WelcomeScreen(
                on_next=lambda: self.router.go("terms"),
                on_cancel=self.close
            )
        )

        self.router.register(
            "terms",
            TermsScreen(
                on_accept=lambda: self.router.go("installers"),
                on_back=lambda: self.router.go("welcome")
            )
        )

        self.router.register(
            "installers",
            InstallerPage(
                on_next=lambda: self.router.go("connection_select"),
                on_back=lambda: self.router.go("terms")
            )
        )

        self.router.register(
            "connection_select",
            ConnectionSelectionScreen(
                on_wireless=lambda: self.router.go("wireless"),
                on_wired=lambda: self.router.go("wired"),
                on_back=lambda: self.router.go("installers")
            )
        )

        self.router.register(
            "wireless",
            WirelessScreen(
                on_back=lambda: self.router.go("connection_select")
            )
        )

        self.router.register(
            "wired",
            WiredScreen(
                on_back=lambda: self.router.go("connection_select")
            )
        )
