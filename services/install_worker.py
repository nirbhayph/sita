from PySide6.QtCore import QThread, Signal
from services.installers.factory import get_platform_installer


class InstallWorker(QThread):
    progress = Signal(int)
    status = Signal(str)
    finished = Signal(bool, str)

    def run(self):
        try:
            installer = get_platform_installer()

            steps = [
                ("Checking package manager", installer.check_package_manager, installer.install_package_manager),
                ("Checking Node.js", installer.check_nodejs, installer.install_nodejs),
                ("Checking npm", installer.check_npm, installer.install_npm),
                ("Checking Appium", installer.check_appium, installer.install_appium),
                ("Checking Android driver", installer.check_android_driver, installer.install_android_driver),
                ("Checking ADB", installer.check_adb, installer.install_adb),
            ]

            total = len(steps)

            for i, (label, check, install) in enumerate(steps, start=1):
                self.status.emit(label)

                if not check():
                    install()

                self.progress.emit(int((i / total) * 100))

            self.status.emit("Installation complete!")
            self.progress.emit(100)
            self.finished.emit(True, "All dependencies installed successfully")

        except Exception as e:
            self.finished.emit(False, str(e))
