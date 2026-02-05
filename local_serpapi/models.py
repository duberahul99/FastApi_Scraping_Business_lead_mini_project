# models.py

"""
This module defines response schemas and typed models for SERP API results.
"""

from pydantic import BaseModel
from typing import Optional, List

class Business(BaseModel):
    name: str
    address: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    facebook: Optional[str]
    instagram: Optional[str]
    linkedin: Optional[str]
    rating: Optional[float]
    sources: List[str]