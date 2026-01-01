import platform
from .macos import MacOSInstaller
from .windows import WindowsInstaller
from .linux import LinuxInstaller


def get_platform_installer():
    system = platform.system()

    if system == "Darwin":
        return MacOSInstaller()
    if system == "Windows":
        return WindowsInstaller()
    if system == "Linux":
        return LinuxInstaller()

    raise RuntimeError(f"Unsupported platform: {system}")
