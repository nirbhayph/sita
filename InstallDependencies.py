import platform
import subprocess
import shutil
import tempfile
import os
import urllib.request
from abc import ABC, abstractmethod
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QProgressBar,
    QTextEdit
)
from PySide6.QtCore import QThread, Signal, Slot


# ==================== Base Platform Installer ====================
class PlatformInstaller(ABC):
    """Abstract base class for platform-specific installation logic"""

    @abstractmethod
    def check_package_manager(self) -> bool:
        pass

    @abstractmethod
    def install_package_manager(self):
        pass

    @abstractmethod
    def install_nodejs(self):
        pass

    @abstractmethod
    def install_npm(self):
        pass

    @abstractmethod
    def install_adb(self):
        pass

    # Common methods that work across all platforms
    @staticmethod
    def check_nodejs() -> bool:
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    @staticmethod
    def check_npm() -> bool:
        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    @staticmethod
    def check_appium() -> bool:
        try:
            result = subprocess.run(['appium', '--version'], capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    @staticmethod
    def check_android_driver() -> bool:
        try:
            result = subprocess.run(['appium', 'driver', 'list', '--installed'],
                                    capture_output=True, text=True, timeout=10)
            output = (result.stdout or '') + '\n' + (result.stderr or '')
            return 'uiautomator2' in output
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    @staticmethod
    def check_adb() -> bool:
        try:
            result = subprocess.run(['adb', 'version'], capture_output=True, text=True, timeout=5)
            output = (result.stdout or '') + '\n' + (result.stderr or '')
            return 'Android Debug Bridge' in output
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    @staticmethod
    def install_appium():
        try:
            subprocess.run(['npm', 'install', '-g', 'appium'], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to install Appium: {e.stderr}")

    @staticmethod
    def install_android_driver():
        try:
            subprocess.run(['appium', 'driver', 'install', 'uiautomator2'], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            if 'is already installed' in e.stderr or 'is already installed' in e.stdout:
                return
            raise Exception(f"Failed to install Android driver: {e.stderr}")


# ==================== macOS Installer ====================
class MacOSInstaller(PlatformInstaller):

    def check_package_manager(self) -> bool:
        return shutil.which('brew') is not None

    def install_package_manager(self):
        try:
            install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            applescript = f'''
                do shell script "{install_cmd}" with administrator privileges
            '''
            subprocess.run(['osascript', '-e', applescript], check=True)

            # Add brew to PATH for this session
            brew_paths = ['/opt/homebrew/bin/brew', '/usr/local/bin/brew']
            for brew_path in brew_paths:
                if os.path.exists(brew_path):
                    os.environ['PATH'] = f"{os.path.dirname(brew_path)}:{os.environ['PATH']}"
                    break
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to install Homebrew: {str(e)}")

    def install_nodejs(self):
        subprocess.run(['brew', 'install', 'node'], check=True)

    def install_npm(self):
        subprocess.run(['brew', 'reinstall', 'node'], check=True)

    def install_adb(self):
        try:
            subprocess.run(['brew', 'install', 'android-platform-tools'], check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to install ADB: {str(e)}")


# ==================== Windows Installer ====================
class WindowsInstaller(PlatformInstaller):

    def check_package_manager(self) -> bool:
        return shutil.which('winget') is not None

    def install_package_manager(self):
        try:
            temp_dir = tempfile.gettempdir()
            installer_url = "https://aka.ms/getwinget"
            msixbundle_path = os.path.join(temp_dir, 'Microsoft.DesktopAppInstaller.msixbundle')

            urllib.request.urlretrieve(installer_url, msixbundle_path)

            powershell_cmd = f'Add-AppxPackage -Path "{msixbundle_path}"'
            subprocess.run(['powershell', '-Command', powershell_cmd], check=True)

            os.remove(msixbundle_path)

            # Add winget to PATH for the current session
            winget_path = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'WindowsApps')
            if os.path.exists(winget_path):
                os.environ['PATH'] = f"{winget_path};{os.environ['PATH']}"
        except Exception as e:
            raise Exception(f"Failed to install winget: {str(e)}")

    def install_nodejs(self):
        subprocess.run(['winget', 'install', '--id', 'OpenJS.NodeJS', '--silent',
                        '--accept-source-agreements', '--accept-package-agreements'], check=True)

    def install_npm(self):
        subprocess.run(['winget', 'install', '--id', 'OpenJS.NodeJS', '--silent',
                        '--accept-source-agreements', '--accept-package-agreements', '--force'], check=True)

    def install_adb(self):
        try:
            subprocess.run(['winget', 'install', '--id', 'Google.PlatformTools', '--silent',
                            '--accept-source-agreements', '--accept-package-agreements'], check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to install ADB: {str(e)}")


# ==================== Linux Installer ====================
class LinuxInstaller(PlatformInstaller):

    def __init__(self):
        self.package_manager = self._detect_package_manager()
        self.sudo_command = self._detect_sudo_gui()

    @staticmethod
    def _detect_package_manager() -> str | None:
        # Detect which package manager is available on the system
        if shutil.which('apt-get'):
            return 'apt'
        elif shutil.which('dnf'):
            return 'dnf'
        elif shutil.which('yum'):
            return 'yum'
        elif shutil.which('pacman'):
            return 'pacman'
        else:
            return None

    @staticmethod
    def _detect_sudo_gui() -> str:
        # Try graphical sudo tools in order of preference
        if shutil.which('pkexec'):  # PolicyKit (most modern, works on most distros)
            return 'pkexec'
        elif shutil.which('gksudo'):  # GTK-based (older Ubuntu/Debian)
            return 'gksudo'
        elif shutil.which('kdesudo'):  # KDE-based
            return 'kdesudo'
        else:
            # Fallback to regular sudo (will require terminal)
            return 'sudo'

    def check_package_manager(self) -> bool:
        return self.package_manager is not None

    def install_package_manager(self):
        raise Exception(
            "No supported package manager found. Please install one of: apt, dnf, yum, or pacman"
        )

    def _run_with_sudo(self, command: list):
        try:
            sudo_cmd = [self.sudo_command] + command
            subprocess.run(sudo_cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to run command with elevated privileges: {str(e)}")

    def install_nodejs(self):
        # Install Node.js using the detected package manager
        if self.package_manager == 'apt':
            # Debian/Ubuntu
            self._run_with_sudo(['apt-get', 'update'])
            self._run_with_sudo(['apt-get', 'install', '-y', 'nodejs', 'npm'])

        elif self.package_manager == 'dnf':
            # Fedora
            self._run_with_sudo(['dnf', 'install', '-y', 'nodejs', 'npm'])

        elif self.package_manager == 'yum':
            # CentOS/RHEL
            self._run_with_sudo(['yum', 'install', '-y', 'epel-release'])
            self._run_with_sudo(['yum', 'install', '-y', 'nodejs', 'npm'])

        elif self.package_manager == 'pacman':
            # Arch Linux
            self._run_with_sudo(['pacman', '-Sy', '--noconfirm', 'nodejs', 'npm'])

        else:
            raise Exception(f"Unsupported package manager: {self.package_manager}")

    def install_npm(self):
        self.install_nodejs()

    def install_adb(self):
        try:
            if self.package_manager == 'apt':
                # Debian/Ubuntu
                self._run_with_sudo(['apt-get', 'update'])
                self._run_with_sudo(['apt-get', 'install', '-y', 'android-tools-adb', 'android-tools-fastboot'])

            elif self.package_manager == 'dnf':
                # Fedora
                self._run_with_sudo(['dnf', 'install', '-y', 'android-tools'])

            elif self.package_manager == 'yum':
                # CentOS/RHEL - needs EPEL repository
                self._run_with_sudo(['yum', 'install', '-y', 'epel-release'])
                self._run_with_sudo(['yum', 'install', '-y', 'android-tools'])

            elif self.package_manager == 'pacman':
                # Arch Linux
                self._run_with_sudo(['pacman', '-S', '--noconfirm', 'android-tools'])

            else:
                raise Exception(f"Unsupported package manager: {self.package_manager}")

        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to install ADB: {str(e)}")


# ==================== Platform Factory ====================
def get_platform_installer() -> PlatformInstaller:
    system = platform.system()

    if system == "Darwin":
        return MacOSInstaller()
    elif system == "Windows":
        return WindowsInstaller()
    elif system == "Linux":
        return LinuxInstaller()
    else:
        raise Exception(f"Unsupported platform: {system}")


# ==================== Install Worker ====================
class InstallWorker(QThread):
    progress = Signal(int)
    status = Signal(str)
    finished = Signal(bool, str)

    def run(self):
        try:
            # Get a platform-specific installer
            installer = get_platform_installer()

            self.status.emit("Checking system requirements...")
            self.progress.emit(5)

            # 1. Check and install the package manager
            if not installer.check_package_manager():
                self.status.emit("Installing package manager...")
                installer.install_package_manager()
            else:
                self.status.emit("Package manager already installed")
            self.progress.emit(12)

            # 2. Check and install Node.js
            if not installer.check_nodejs():
                self.status.emit("Installing Node.js...")
                installer.install_nodejs()
            else:
                self.status.emit("Node.js already installed")
            self.progress.emit(25)

            # 3. Check and install npm
            if not installer.check_npm():
                self.status.emit("Installing npm...")
                installer.install_npm()
            else:
                self.status.emit("npm already installed")
            self.progress.emit(35)

            # 4. Check and install Appium
            if not installer.check_appium():
                self.status.emit("Installing Appium server...")
                installer.install_appium()
            else:
                self.status.emit("Appium already installed")
            self.progress.emit(50)

            # 5. Check and install the Android driver
            if not installer.check_android_driver():
                self.status.emit("Installing Android driver (uiautomator2)...")
                installer.install_android_driver()
            else:
                self.status.emit("Android driver already installed")
            self.progress.emit(65)

            # 6. Check and install ADB
            if not installer.check_adb():
                self.status.emit("Installing ADB (Android Debug Bridge)...")
                installer.install_adb()
            else:
                self.status.emit("ADB already installed")
            self.progress.emit(75)

            # 7. Verify Appium
            self.status.emit("Verifying Appium installation...")
            if not installer.check_appium():
                raise Exception("Appium verification failed")
            self.progress.emit(85)

            # 8. Verify Android driver
            self.status.emit("Verifying Android driver installation...")
            if not installer.check_android_driver():
                raise Exception("Android driver verification failed")
            self.progress.emit(92)

            # 9. Verify ADB
            self.status.emit("Verifying ADB installation...")
            if not installer.check_adb():
                raise Exception("ADB verification failed")
            self.progress.emit(100)

            self.status.emit("Installation complete!")
            self.finished.emit(True,
                               "All dependencies installed successfully!\n")

        except Exception as e:
            self.finished.emit(False, f"Installation failed: {str(e)}")


# ==================== UI Component ====================
class InstallerPage(QWidget):

    def __init__(self, on_next=None, on_back=None):
        super().__init__()
        self.next_btn = None
        self.install_btn = None
        self.back_btn = None
        self.log_text = None
        self.progress_bar = None
        self.status_label = None
        self.title_label = None
        self.on_next_callback = on_next
        self.on_back_callback = on_back
        self.init_ui()
        self.worker = None

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("Device Host Setup - Installing Dependencies")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.title_label)

        info_label = QLabel("This will install Appium server and Android driver on your device.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(info_label)

        self.status_label = QLabel("Click 'Install' to begin installation")
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        layout.addWidget(self.log_text)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.back_btn = QPushButton("Back")
        self.install_btn = QPushButton("Install")
        self.next_btn = QPushButton("Next")
        self.next_btn.setEnabled(False)

        self.back_btn.clicked.connect(self.on_back)
        self.install_btn.clicked.connect(self.on_install)
        self.next_btn.clicked.connect(self.on_next)

        btn_layout.addWidget(self.back_btn)
        btn_layout.addWidget(self.install_btn)
        btn_layout.addWidget(self.next_btn)

        layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def on_install(self):
        self.install_btn.setEnabled(False)
        self.back_btn.setEnabled(False)
        self.log_text.clear()

        self.worker = InstallWorker()
        self.worker.progress.connect(self.update_progress)
        self.worker.status.connect(self.update_status)
        self.worker.finished.connect(self.on_installation_finished)
        self.worker.start()

    @Slot(int)
    def update_progress(self, value):
        self.progress_bar.setValue(value)

    @Slot(str)
    def update_status(self, message):
        self.status_label.setText(message)
        self.log_text.append(f"• {message}")

    @Slot(bool, str)
    def on_installation_finished(self, success, message):
        self.log_text.append(f"\n{message}")

        if success:
            self.status_label.setText("Installation completed successfully!")
            self.next_btn.setEnabled(True)
            self.install_btn.setEnabled(False)
        else:
            self.status_label.setText("Installation failed")
            self.install_btn.setEnabled(True)
            self.back_btn.setEnabled(True)

    def on_back(self):
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        if self.on_back_callback:
            self.on_back_callback()

    def on_next(self):
        if self.on_next_callback:
            self.on_next_callback()