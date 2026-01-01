import shutil, os, subprocess
from .base import PlatformInstaller


class MacOSInstaller(PlatformInstaller):

    def check_package_manager(self) -> bool:
        return shutil.which('brew') is not None

    def install_package_manager(self):
        cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        subprocess.run(['osascript', '-e', f'do shell script "{cmd}" with administrator privileges'], check=True)

        for path in ['/opt/homebrew/bin', '/usr/local/bin']:
            if os.path.exists(path):
                os.environ['PATH'] = f"{path}:{os.environ['PATH']}"

    def install_nodejs(self):
        subprocess.run(['brew', 'install', 'node'], check=True)

    def install_npm(self):
        subprocess.run(['brew', 'reinstall', 'node'], check=True)

    def install_adb(self):
        subprocess.run(['brew', 'install', 'android-platform-tools'], check=True)
