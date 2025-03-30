from dataclasses import dataclass

@dataclass
class ImageEntity:
    image_name: str
    image_data: bytes
    metadata: dict | None = None