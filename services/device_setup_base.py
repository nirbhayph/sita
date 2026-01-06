from abc import ABC
from services.adb_service import AdbService
from services.device_info import DeviceInfo


class BaseDeviceSetupController(ABC):
    """
    Shared device-related helpers for setup controllers
    """

    def _get_connected_device(self) -> DeviceInfo | None:
        device_id = AdbService.get_connected_device_id()
        if not device_id:
            return None

        model = AdbService.get_device_model(device_id)
        return DeviceInfo(
            device_id=device_id,
            model=model
        )