from pathlib import Path

ATTACHMENTS_DIR = Path("features") / "attachments"

def read_attachment(file_name: str) -> str:
    file_path = ATTACHMENTS_DIR / file_name

    if not file_path.is_file():
        raise FileNotFoundError(f"Attachment file not found: {file_path}")

    return file_path.read_text(encoding="utf-8").strip()

def read_file_path(file_name: str) -> str:
    file_path = (ATTACHMENTS_DIR / file_name).resolve()
    print("File path:", file_path)

    if not file_path.is_file():
        raise FileNotFoundError(f"Attachment file not found: {file_path}")

    return str(file_path)