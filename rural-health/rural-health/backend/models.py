# models.py
from pydantic import BaseModel, Field
from typing import Optional

class PatientCreate(BaseModel):
    name: str = Field(..., example="Ravi Kumar")
    age: Optional[int] = Field(None, example=35)
    phone: Optional[str] = Field(None, example="9876543210")
    symptoms: Optional[str] = Field(None, example="fever, headache")

class PatientDB(PatientCreate):
    id: str
