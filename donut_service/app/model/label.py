from pydantic import BaseModel
from typing import Optional, Dict

class StRequest(BaseModel):
    nr: Optional[str] = None
    date: Optional[str] = None
    zr: Optional[str] = None
    donated_blood: Optional[str] = None

class LabelRequest(BaseModel):
    image_code: str
    surname: Optional[str] = None
    name: Optional[str] = None
    date_of_birth: Optional[str] = None
    iii_st: Optional[StRequest] = None
    ii_st: Optional[StRequest] = None
    i_st: Optional[StRequest] = None
    duplicate: Optional[str] = None