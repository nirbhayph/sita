import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QStackedWidget
)
from TermsScreen import TermsScreen
from WelcomeScreen import WelcomeScreen
from WirelessScreen import WirelessScreen
from ConnectionSelectionScreen import ConnectionSelectionScreen
from WiredScreen import WiredScreen
from InstallDependencies import InstallerPage

class Installer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Device Host Setup")
        self.setFixedSize(1000, 600)

        self.stack = QStackedWidget(self)

        self.welcome_screen = WelcomeScreen(
            on_next=self.show_terms,
            on_cancel=self.close
        )

        self.terms_screen = TermsScreen(
            on_accept=self.show_installer,
            on_back=self.show_welcome
        )

        self.installer_screen = InstallerPage(
            on_next=self.show_connection_selection,
            on_back=self.show_terms
        )

        self.connection_select_screen = ConnectionSelectionScreen(
            on_wireless=self.show_wireless,
            on_wired=self.show_wired,
            on_back=self.show_installer
        )

        self.wireless_screen = WirelessScreen(on_back=self.show_connection_selection)
        self.wired_screen = WiredScreen(on_back=self.show_connection_selection)

        for screen in [
            self.welcome_screen,
            self.terms_screen,
            self.installer_screen,
            self.connection_select_screen,
            self.wireless_screen,
            self.wired_screen
        ]:
            self.stack.addWidget(screen)

        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

    def show_welcome(self):
        self.stack.setCurrentWidget(self.welcome_screen)

    def show_terms(self):
        self.stack.setCurrentWidget(self.terms_screen)

    def show_installer(self):
        self.stack.setCurrentWidget(self.installer_screen)

    def show_connection_selection(self):
        self.stack.setCurrentWidget(self.connection_select_screen)

    def show_wireless(self):
        self.stack.setCurrentWidget(self.wireless_screen)

    def show_wired(self):
        self.stack.setCurrentWidget(self.wired_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Installer()
    window.show()
    sys.exit(app.exec())
