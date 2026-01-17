# models.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class TaxPayer(BaseModel):
    name: str
    pan_number: str = Field(..., min_length=10, max_length=10, pattern=r"[A-Z]{5}[0-9]{4}[A-Z]{1}")
    age: int
    salary_income: float
    interest_income: float = 0.0
    section_80c_deductions: float = 0.0 # PF, LIC, etc.
    section_80d_deductions: float = 0.0 # Health Insurance

    class Config:
        # This helps the AI understand what format we want
        json_schema_extra = {
            "example": {
                "name": "Itishree Khadiratna",
                "pan_number": "ABCDE1234F",
                "age": 25,
                "salary_income": 850000,
                "section_80c_deductions": 150000
            }
        }