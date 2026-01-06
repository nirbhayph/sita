from services.device_setup.device_setup_base import BaseDeviceSetupController
from services.adb.adb_service import AdbService


class WiredSetupState:
    def __init__(self):
        self.device_connected = False
        self.device_model = None
        self.usb_debugging_enabled = False


class WiredSetupController(BaseDeviceSetupController):
    def get_state(self) -> WiredSetupState:
        state = WiredSetupState()

        device_id = AdbService.get_usb_device_id()
        if not device_id:
            return state

        state.device_connected = True
        state.device_model = AdbService.get_device_model(device_id)
        state.usb_debugging_enabled = AdbService.is_usb_debugging_enabled(device_id)

        return state
