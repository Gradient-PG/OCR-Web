from pydantic import BaseModel
from typing import Optional, Dict

class TaskRequest(BaseModel):
    image_code: str