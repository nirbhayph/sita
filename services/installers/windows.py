import shutil
import subprocess
import tempfile
import os
import urllib.request

from .base import PlatformInstaller


class WindowsInstaller(PlatformInstaller):

    def check_package_manager(self) -> bool:
        return shutil.which("winget") is not None

    def install_package_manager(self):
        try:
            temp_dir = tempfile.gettempdir()
            installer_url = "https://aka.ms/getwinget"
            bundle_path = os.path.join(
                temp_dir, "Microsoft.DesktopAppInstaller.msixbundle"
            )

            urllib.request.urlretrieve(installer_url, bundle_path)

            subprocess.run(
                ["powershell", "-Command", f'Add-AppxPackage -Path "{bundle_path}"'],
                check=True
            )

            os.remove(bundle_path)

            # Ensure winget is in PATH for current session
            winget_path = os.path.join(
                os.environ.get("LOCALAPPDATA", ""),
                "Microsoft",
                "WindowsApps"
            )
            if os.path.exists(winget_path):
                os.environ["PATH"] = f"{winget_path};{os.environ['PATH']}"

        except Exception as e:
            raise RuntimeError(f"Failed to install winget: {e}")

    def install_nodejs(self):
        subprocess.run(
            [
                "winget", "install",
                "--id", "OpenJS.NodeJS",
                "--silent",
                "--accept-source-agreements",
                "--accept-package-agreements"
            ],
            check=True
        )

    def install_npm(self):
        # npm comes with Node.js on Windows
        self.install_nodejs()

    def install_adb(self):
        subprocess.run(
            [
                "winget", "install",
                "--id", "Google.PlatformTools",
                "--silent",
                "--accept-source-agreements",
                "--accept-package-agreements"
            ],
            check=True
        )
