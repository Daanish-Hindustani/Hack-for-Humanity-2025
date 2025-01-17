from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HostFamily(Base):
    __tablename__ = 'host_families'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_info = Column(String)
    number_of_people = Column(Integer)
    pet_friendly = Column(Boolean, default=False)
    location = Column(String)
    matched = Column(Boolean, default=False)

class DisplacedFamily(Base):
    __tablename__ = 'displaced_families'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_info = Column(String)
    number_of_family_members = Column(Integer)
    has_pets = Column(Boolean, default=False)
    location = Column(String)
    matched = Column(Boolean, default=False)
