from pydantic import BaseModel, Field, EmailStr
from models import UserTypeEnum

class User(BaseModel):
    """
    Represents a generalized user model with attributes for name, 
    contact information, and user type.
    """
    name: str = Field(..., max_length=100, description="The name of the user.")
    email: EmailStr = Field(..., description="The email address of the user.")
    contact_info: str = Field(..., max_length=255, description="Contact details of the user.")
    family_size: int = Field(..., ge=1, description="The number of family members.")
    has_pets: bool = Field(default=False, description="Indicates if the user has pets.")
    user_type: UserTypeEnum = Field(..., description="The type of user (e.g., host family or displaced family).")
    location: str = Field(..., max_length=255, description="The location of the user.")
    is_matched: bool = Field(default=False, description="Indicates if the user has been matched.")
    hashed_password: str = Field(..., min_length=8, description="The hashed password for the user's account.")

    class Config:
        from_attributes = True
        populate_by_name = True
