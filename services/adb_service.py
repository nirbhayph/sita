import subprocess


class AdbService:
    @staticmethod
    def get_connected_device_id():
        try:
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True,
                text=True
            )

            for line in result.stdout.splitlines()[1:]:
                if "\tdevice" in line:
                    return line.split("\t")[0]

            return None
        except Exception:
            return None

    @staticmethod
    def get_device_model(device_id: str) -> str:
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "shell", "getprop", "ro.product.model"],
                capture_output=True,
                text=True,
                timeout=2
            )
            return result.stdout.strip() or "Unknown device"
        except Exception:
            return "Unknown device"

    @staticmethod
    def is_usb_debugging_enabled(device_id: str) -> bool:
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "shell", "echo", "ok"],
                capture_output=True,
                text=True,
                timeout=2
            )
            return result.stdout.strip() == "ok"
        except Exception:
            return False

    @staticmethod
    def pair_device(ip_port: str, code: str) -> tuple[bool, str]:
        try:
            proc = subprocess.Popen(
                ["adb", "pair", ip_port],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = proc.communicate(code + "\n", timeout=15)

            if proc.returncode == 0:
                return True, stdout.strip()

            return False, stderr.strip() or stdout.strip()

        except Exception as e:
            return False, str(e)

    @staticmethod
    def get_wireless_device():
        try:
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True,
                text=True
            )

            for line in result.stdout.splitlines()[1:]:
                if ":" in line:
                    device_id, status = line.strip().split("\t", 1)
                    return device_id, status

            return None, None
        except Exception:
            return None, None

