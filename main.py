import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QStackedWidget
)
from TermsScreen import TermsScreen
from FinishScreen import FinishScreen
from WelcomeScreen import WelcomeScreen

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
            on_accept=self.show_finish,
            on_back=self.show_welcome
        )

        self.finish_screen = FinishScreen(
            on_back=self.show_terms
        )

        self.stack.addWidget(self.welcome_screen)
        self.stack.addWidget(self.terms_screen)
        self.stack.addWidget(self.finish_screen)

        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

        self.stack.setCurrentWidget(self.welcome_screen)

    def show_welcome(self):
        self.stack.setCurrentWidget(self.welcome_screen)

    def show_terms(self):
        self.stack.setCurrentWidget(self.terms_screen)

    def show_finish(self):
        self.stack.setCurrentWidget(self.finish_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Installer()
    window.show()
    sys.exit(app.exec())
