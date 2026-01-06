import random
import string
import subprocess
import qrcode
from dataclasses import dataclass

from services.paths import QR_CODE_PATH


@dataclass
class QrCodeData:
    service_name: str
    password: str
    pairing_string: str
    image_path: str


class WifiQrPairingService:
    SERVICE_PREFIX = "studio-"

    @staticmethod
    def _random_string(length: int) -> str:
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    # ✅ REMOVE output_path argument
    def generate_qr_code(self) -> QrCodeData:
        service = self.SERVICE_PREFIX + self._random_string(10)
        password = self._random_string(12)

        pairing_string = f"WIFI:T:ADB;S:{service};P:{password};;"

        img = qrcode.make(pairing_string)
        img.save(QR_CODE_PATH)

        return QrCodeData(
            service_name=service,
            password=password,
            pairing_string=pairing_string,
            image_path=str(QR_CODE_PATH),  # ✅ correct path
        )

    def check_mdns_support(self) -> bool:
        result = subprocess.run(
            ["adb", "mdns", "check"],
            capture_output=True,
            text=True
        )
        return "mdns daemon version" in result.stdout.lower()

    def scan_mdns_services(self):
        result = subprocess.run(
            ["adb", "mdns", "services"],
            capture_output=True,
            text=True
        )

        services = []
        for line in result.stdout.splitlines():
            if "_adb-tls-pairing._tcp" in line:
                parts = line.split()
                service_name = parts[0]
                ip, port = parts[-1].split(":")
                services.append((service_name, ip, int(port)))

        return services

    def pair(self, ip: str, port: int, password: str) -> bool:
        proc = subprocess.Popen(
            ["adb", "pair", f"{ip}:{port}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        proc.communicate(password + "\n", timeout=15)
        return proc.returncode == 0
