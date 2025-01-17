import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi_sqlalchemy import DBSessionMiddleware, db
from schema import HostFamily as SchemaHostFamily
from schema import DisplacedFamily as SchemaDisplacedFamily
from models import HostFamily as ModelHostFamily
from models import DisplacedFamily as ModelDisplacedFamily
import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()


app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

# APIs 

# Base route
@app.get("/")
async def root():
    return {"message": "hello world"}

# Register family (Create a new displaced family)
@app.post('/family/', response_model=SchemaDisplacedFamily)
async def register_family(family: SchemaDisplacedFamily):
    db_family = ModelDisplacedFamily(
        name=family.name,
        contact_info=family.contact_info,
        number_of_family_members=family.number_of_family_members,
        has_pets=family.has_pets,
        location=family.location,
        matched=family.matched
    )

    db.session.add(db_family)
    db.session.commit()
    return db_family

# Get all families
@app.get('/family/')
async def get_families():
    families = db.session.query(ModelDisplacedFamily).all()
    return families

# Get a single family by ID
@app.get('/family/{family_id}')
async def get_family(family_id: int):
    family = db.session.query(ModelDisplacedFamily).filter(ModelDisplacedFamily.id == family_id).first()
    
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    
    return family

# @app.put('/family/{family_id}')

@app.delete('/family/{family_id}')
async def delete_family(family_id: int):
    family = db.query(ModelDisplacedFamily).filter(ModelDisplacedFamily.id == family_id).first()
    
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    
    db.delete(family)
    
    db.commit()
    
    return {"message": f"Family with ID {family_id} deleted successfully"}





# Register host (Create a new host family)
@app.post('/host/', response_model=SchemaHostFamily)
async def register_host(host: SchemaHostFamily):
    db_host = ModelHostFamily(
        name=host.name,
        contact_info=host.contact_info,
        number_of_people=host.number_of_people,  
        pet_friendly=host.pet_friendly,  
        location=host.location,
        matched=host.matched
    )

    db.session.add(db_host)
    db.session.commit()
    return db_host


@app.get('/host/')
async def get_hosts():
    hosts = db.session.query(ModelHostFamily).all()
    return hosts

# Start the application
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
