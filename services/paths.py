from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

QR_CODE_DIR = PROJECT_ROOT / "resources" / "generated_qr_code"
QR_CODE_DIR.mkdir(parents=True, exist_ok=True)

QR_CODE_PATH = QR_CODE_DIR / "wifi_pairing_qr.png"
