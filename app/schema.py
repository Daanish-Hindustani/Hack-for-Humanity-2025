from pydantic import BaseModel, Field


class HostFamily(BaseModel):
    
    name: str
    contact_info: str
    number_of_people: int
    pet_friendly : bool
    location : str
    matched : bool

    class Config:
        from_attributes = True

class DisplacedFamily(BaseModel):
    
    name: str
    contact_info: str
    number_of_family_members: int
    has_pets : bool
    location : str
    matched : bool

    class Config:
        from_attributes = True



        