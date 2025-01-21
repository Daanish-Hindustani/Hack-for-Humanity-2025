import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi_sqlalchemy import DBSessionMiddleware, db
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from schema import User as SchemaUser
from models import User as ModelUser
import os
from dotenv import load_dotenv
from auth import get_current_user_from_cookie, create_access_token, verify_password, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES

load_dotenv('../.env')

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


# Endpoint to retrieve token via username and password
@app.post("/token")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.session.query(ModelUser).filter(ModelUser.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    
    # Set the token in cookies
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    
    return {"access_token": access_token, "token_type": "bearer"}


# Home
@app.get("/login", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Creates a user (like registering)
@app.post('/signup/', response_model=SchemaUser)
async def create_user(user: SchemaUser):
    hashed_password = get_password_hash(user.hashed_password)
    db_user = ModelUser(
        name=user.name,
        email=user.email,
        contact_info=user.contact_info,
        family_size=user.family_size,
        has_pets=user.has_pets,
        user_type=user.user_type,
        location=user.location,
        is_matched=user.is_matched,
        hashed_password=hashed_password,
        matched_id=user.matched_id
    )
    db.session.add(db_user)
    db.session.commit()
    return db_user

# Gets current user
@app.get('/myinfo/', response_model=SchemaUser)
async def read_users_me(current_user: SchemaUser = Depends(get_current_user_from_cookie)):
    return current_user

@app.get('/user/{user_id}', response_model=SchemaUser)
async def get_user(user_id: int, current_user: SchemaUser = Depends(get_current_user_from_cookie)):
    credentials_exception = HTTPException(
        status_code=404,
        detail="Could not find user",
    )
    user = db.session.query(ModelUser).filter_by(id=user_id).first()
    if not user:
        raise credentials_exception
    return user

# Gets all users
@app.get('/users/', response_model=list[SchemaUser])
async def get_users(current_user: SchemaUser = Depends(get_current_user_from_cookie)):
    users = db.session.query(ModelUser).all()
    return users

# Start the application
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
