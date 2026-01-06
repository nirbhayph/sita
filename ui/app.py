from enum import Enum

from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget

from navigation.router import Router

from ui.screens.welcome import WelcomeScreen
from ui.screens.terms import TermsScreen
from ui.screens.installers import InstallerPage
from ui.screens.connection_select import ConnectionSelectionScreen
from ui.screens.wireless import WirelessScreen
from ui.screens.wired import WiredScreen


class InstallerApp(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._setup_navigation()
        self._setup_layout()

        self.router.go(Screen.CONNECTION_SELECT)

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
            Screen.WELCOME,
            WelcomeScreen(
                on_next=lambda: self.router.go(Screen.TERMS),
                on_cancel=self.close
            )
        )

        self.router.register(
            Screen.TERMS,
            TermsScreen(
                on_accept=lambda: self.router.go(Screen.INSTALLERS),
                on_back=lambda: self.router.go(Screen.WELCOME)
            )
        )

        self.router.register(
            Screen.INSTALLERS,
            InstallerPage(
                on_next=lambda: self.router.go(Screen.CONNECTION_SELECT),
                on_back=lambda: self.router.go(Screen.TERMS)
            )
        )

        self.router.register(
            Screen.CONNECTION_SELECT,
            ConnectionSelectionScreen(
                on_wireless=lambda: self.router.go(Screen.WIRELESS),
                on_wired=lambda: self.router.go(Screen.WIRED),
                on_back=lambda: self.router.go(Screen.INSTALLERS)
            )
        )

        self.router.register(
            Screen.WIRELESS,
            WirelessScreen(
                on_back=lambda: self.router.go(Screen.CONNECTION_SELECT)
            )
        )

        self.router.register(
            Screen.WIRED,
            WiredScreen(
                on_back=lambda: self.router.go(Screen.CONNECTION_SELECT)
            )
        )

class Screen(str, Enum):
    WELCOME = "welcome"
    TERMS = "terms"
    INSTALLERS = "installers"
    CONNECTION_SELECT = "connection_select"
    WIRELESS = "wireless"
    WIRED = "wired"