import subprocess
import re
from abc import ABC, abstractmethod


class PlatformInstaller(ABC):

    @abstractmethod
    def check_package_manager(self) -> bool: ...

    @abstractmethod
    def install_package_manager(self): ...

    @abstractmethod
    def install_nodejs(self): ...

    @abstractmethod
    def install_npm(self): ...

    @abstractmethod
    def install_adb(self): ...

    # ---------- Common checks ----------

    @staticmethod
    def _check_version(cmd, pattern) -> bool:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            output = (result.stdout or '') + (result.stderr or '')
            return bool(re.search(pattern, output))
        except Exception:
            return False

    @classmethod
    def check_nodejs(cls) -> bool:
        return cls._check_version(['node', '--version'], r'\bv\d+\.\d+\.\d+\b')

    @classmethod
    def check_npm(cls) -> bool:
        return cls._check_version(['npm', '--version'], r'\b\d+\.\d+\.\d+\b')

    @classmethod
    def check_appium(cls) -> bool:
        return cls._check_version(['appium', '--version'], r'\b\d+\.\d+\.\d+\b')

    # ✅ ADD THIS (it was missing)
    @staticmethod
    def check_android_driver() -> bool:
        try:
            result = subprocess.run(
                ['appium', 'driver', 'list', '--installed'],
                capture_output=True,
                text=True,
                timeout=10
            )
            output = (result.stdout or '') + (result.stderr or '')
            return 'uiautomator2' in output
        except Exception:
            return False

    # ✅ KEEP THIS version (idempotent)
    @staticmethod
    def install_android_driver():
        try:
            subprocess.run(
                ['appium', 'driver', 'install', 'uiautomator2'],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            output = (e.stdout or '') + (e.stderr or '')
            if "already installed" in output.lower():
                return
            raise RuntimeError(
                f"Failed to install Android driver: {output.strip()}"
            )

    @staticmethod
    def check_adb() -> bool:
        try:
            result = subprocess.run(['adb', 'version'], capture_output=True, text=True)
            return 'Android Debug Bridge' in result.stdout
        except Exception:
            return False

    @staticmethod
    def install_appium():
        subprocess.run(['npm', 'install', '-g', 'appium'], check=True)
