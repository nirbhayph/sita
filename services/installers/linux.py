import shutil
import subprocess

from .base import PlatformInstaller


class LinuxInstaller(PlatformInstaller):

    def __init__(self):
        self.package_manager = self._detect_package_manager()
        self.sudo = self._detect_sudo()

    # ---------- Detection ----------

    @staticmethod
    def _detect_package_manager():
        if shutil.which("apt-get"):
            return "apt"
        if shutil.which("dnf"):
            return "dnf"
        if shutil.which("yum"):
            return "yum"
        if shutil.which("pacman"):
            return "pacman"
        return None

    @staticmethod
    def _detect_sudo():
        if shutil.which("pkexec"):
            return "pkexec"
        if shutil.which("gksudo"):
            return "gksudo"
        if shutil.which("kdesudo"):
            return "kdesudo"
        return "sudo"

    # ---------- Core ----------

    def check_package_manager(self) -> bool:
        return self.package_manager is not None

    def install_package_manager(self):
        raise RuntimeError(
            "No supported package manager found. "
            "Install apt, dnf, yum, or pacman manually."
        )

    def _run(self, command: list):
        subprocess.run([self.sudo] + command, check=True)

    # ---------- Installers ----------

    def install_nodejs(self):
        if self.package_manager == "apt":
            self._run(["apt-get", "update"])
            self._run(["apt-get", "install", "-y", "nodejs", "npm"])

        elif self.package_manager == "dnf":
            self._run(["dnf", "install", "-y", "nodejs", "npm"])

        elif self.package_manager == "yum":
            self._run(["yum", "install", "-y", "epel-release"])
            self._run(["yum", "install", "-y", "nodejs", "npm"])

        elif self.package_manager == "pacman":
            self._run(["pacman", "-Sy", "--noconfirm", "nodejs", "npm"])

        else:
            raise RuntimeError("Unsupported Linux distribution")

    def install_npm(self):
        # npm comes with Node.js
        self.install_nodejs()

    def install_adb(self):
        if self.package_manager == "apt":
            self._run([
                "apt-get", "install", "-y",
                "android-tools-adb", "android-tools-fastboot"
            ])

        elif self.package_manager == "dnf":
            self._run(["dnf", "install", "-y", "android-tools"])

        elif self.package_manager == "yum":
            self._run(["yum", "install", "-y", "android-tools"])

        elif self.package_manager == "pacman":
            self._run(["pacman", "-S", "--noconfirm", "android-tools"])

        else:
            raise RuntimeError("Unsupported Linux distribution")
