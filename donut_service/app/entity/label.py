from dataclasses import dataclass, field
from dataclasses import asdict
from typing import Optional
from ..model.label import StRequest

def to_st_field(data):
    if isinstance(data, dict):
        return StField(**data)  # Convert dictionary to StField
    if isinstance(data, StRequest):
            # Convert StRequest (Pydantic model) to StField (dataclass)
            return StField(
                nr=data.nr,
                date=data.date,
                zr=data.zr,
                donated_blood=data.donated_blood
            )
    return data  # Return as-is if already an instance of StField or None

@dataclass
class StField:
    nr: Optional[str] = None
    date: Optional[str] = None
    zr: Optional[str] = None
    donated_blood: Optional[str] = None

@dataclass
class LabelEntity:
    image_code: str
    surname: Optional[str] = None
    name: Optional[str] = None
    date_of_birth: Optional[str] = None
    iii_st: Optional[StField] = field(default_factory=StField)
    ii_st: Optional[StField] = field(default_factory=StField)
    i_st: Optional[StField] = field(default_factory=StField)
    duplicate: Optional[str] = None
    
    def to_dict(self) -> dict:
        """
        Convert the LabelEntity object to a dictionary for JSON serialization.
        """
        return {
            "image_code": self.image_code,
            "gt_parse": {
                "Surname": self.surname,
                "Name": self.name,
                "Date of birth": self.date_of_birth,
                "III st.": asdict(self.iii_st) if self.iii_st else None,
                "II st.": asdict(self.ii_st) if self.ii_st else None,
                "I st.": asdict(self.i_st) if self.i_st else None,
                "Duplicate": self.duplicate,
            }
        }