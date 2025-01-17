from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()

class UserTypeEnum(str, PyEnum):
    HOST_FAMILY = "host_family"
    DISPLACED_FAMILY = "displaced_family"

class User(Base):
    """
    Represents a user in the system. Users can either be host families 
    or displaced families, with various attributes like location, 
    contact info, and family size.
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    contact_info = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    is_matched = Column(Boolean, default=False)
    name = Column(String(100), index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    user_type = Column(Enum(UserTypeEnum), nullable=False)
    has_pets = Column(Boolean, default=False)
    family_size = Column(Integer, nullable=True)
    matched_id = Column(String, nullable=True, default=None)