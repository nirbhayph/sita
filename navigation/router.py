from PySide6.QtWidgets import QStackedWidget


class Router:
    def __init__(self, stack: QStackedWidget):
        self.stack = stack
        self.screens = {}

    def register(self, name: str, widget):
        self.screens[name] = widget
        self.stack.addWidget(widget)

    def go(self, name: str):
        self.stack.setCurrentWidget(self.screens[name])
