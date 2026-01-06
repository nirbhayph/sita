from services.device_setup_base import BaseDeviceSetupController
from services.wifi_qr_pairing import WifiQrPairingService


class WirelessSetupController(BaseDeviceSetupController):
    def __init__(self):
        self.qr_service = WifiQrPairingService()
        self.qr_data = None
        self.pairing_in_progress = False

    def start_qr_pairing(self):
        if not self.qr_service.check_mdns_support():
            raise RuntimeError(
                "ADB mDNS not supported. Please update platform-tools."
            )

        self.qr_data = self.qr_service.generate_qr_code()
        self.pairing_in_progress = True
        return self.qr_data

    def poll_for_device(self) -> tuple[bool, str | None]:
        if not self.pairing_in_progress or not self.qr_data:
            return False, None

        services = self.qr_service.scan_mdns_services()

        for service_name, ip, port in services:
            if service_name == self.qr_data.service_name:
                success = self.qr_service.pair(
                    ip=ip,
                    port=port,
                    password=self.qr_data.password
                )

                if success:
                    self.pairing_in_progress = False
                    device = self._get_connected_device()
                    return True, device.model if device else "Android device"

        return False, None