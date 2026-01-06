from services.adb.adb_service import AdbService


class DeviceDiscoveryService:
    @staticmethod
    def get_wireless_devices() -> list[str]:
        devices = []

        for device in AdbService.get_all_devices():
            if (
                device["is_wireless"]
                and device["status"] == "device"
            ):
                model = AdbService.get_device_model(device["id"])
                devices.append(model)

        return devices

    @staticmethod
    def get_wired_devices() -> list[str]:
        devices = []

        for device in AdbService.get_all_devices():
            if (
                device["is_usb"]
                and device["status"] == "device"
            ):
                model = AdbService.get_device_model(device["id"])
                devices.append(model)

        return devices
