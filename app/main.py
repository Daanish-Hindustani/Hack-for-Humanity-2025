import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db
from schema import User as SchemaUser
from models import User as ModelUser
import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

# Base route
@app.get("/")
async def root():
    return {"message": "Welcome to the User Management API"}

# Create a new user
@app.post('/users/', response_model=SchemaUser)
async def create_user(user: SchemaUser):
    db_user = ModelUser(
        name=user.name,
        email=user.email,
        contact_info=user.contact_info,
        family_size=user.family_size,
        has_pets=user.has_pets,
        user_type=user.user_type,
        location=user.location,
        is_matched=user.is_matched,
        hashed_password=user.hashed_password
    )

    db.session.add(db_user)
    db.session.commit()
    return db_user

# Get all users
@app.get('/users/')
async def get_users():
    users = db.session.query(ModelUser).all()
    return users

# Get a single user by ID
@app.get('/users/{user_id}')
async def get_user(user_id: int):
    user = db.session.query(ModelUser).filter(ModelUser.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

# Update a user by ID
@app.put('/users/{user_id}', response_model=SchemaUser)
async def update_user(user_id: int, updated_user: SchemaUser):
    user = db.session.query(ModelUser).filter(ModelUser.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = updated_user.name
    user.email = updated_user.email
    user.contact_info = updated_user.contact_info
    user.family_size = updated_user.family_size
    user.has_pets = updated_user.has_pets
    user.user_type = updated_user.user_type
    user.location = updated_user.location
    user.is_matched = updated_user.is_matched
    user.hashed_password = updated_user.hashed_password

    db.session.commit()
    return user

# Delete a user by ID
@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    user = db.session.query(ModelUser).filter(ModelUser.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.session.delete(user)
    db.session.commit()

    return {"message": f"User with ID {user_id} deleted successfully"}

# Start the application
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
