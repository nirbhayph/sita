from dataclasses import dataclass

@dataclass(frozen=True)
class DeviceInfo:
    device_id: str
    model: str
