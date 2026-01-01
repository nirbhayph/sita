from services.adb_service import AdbService


class WirelessSetupState:
    def __init__(self):
        self.device_connected = False
        self.device_name = None
        self.waiting_for_connection = False
        self.error = None


class WirelessSetupController:
    def __init__(self):
        self.waiting_for_connection = False

    def pair(self, ip_port: str, code: str) -> tuple[bool, str]:
        success, message = AdbService.pair_device(ip_port, code)
        if success:
            self.waiting_for_connection = True
        return success, message

    def poll(self) -> WirelessSetupState:
        state = WirelessSetupState()
        state.waiting_for_connection = self.waiting_for_connection

        device_id, status = AdbService.get_wireless_device()

        if not device_id:
            return state

        if status == "device":
            state.device_connected = True
            state.device_name = AdbService.get_device_model(device_id)
            self.waiting_for_connection = False
        elif status == "unauthorized":
            state.error = "Device connected but not authorized"

        return state
