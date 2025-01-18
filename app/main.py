import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi_sqlalchemy import DBSessionMiddleware, db
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from schema import User as SchemaUser
from models import User as ModelUser
import os
from dotenv import load_dotenv

load_dotenv('../.env')

# Configuration
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

#creates access token 
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta  # Use timezone.utc
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)  # Use timezone.utc
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#validate user via token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.session.query(ModelUser).filter(ModelUser.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

# Routes

#endpoint to retrive token via username and password
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.session.query(ModelUser).filter(ModelUser.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

#home
@app.get("/")
async def root():
    return {"message": "Welcome to the User Management API"}

#creates a user(like registering)
@app.post('/users/', response_model=SchemaUser)
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


#gets current user
@app.get('/myinfo/', response_model=SchemaUser)
async def read_users_me(current_user: SchemaUser = Depends(get_current_user)):
    return current_user

@app.get('/user/{user_id}', response_model=SchemaUser)
async def get_user(user_id: int, current_user: SchemaUser = Depends(get_current_user)):
    credentials_exception = HTTPException(
        status_code=404,
        detail="Could not find user",
    )
    user = db.session.query(ModelUser).filter_by(id=user_id).first()
    if not user:
        return credentials_exception
    return user
    

#gets all users
@app.get('/users/', response_model=list[SchemaUser])
async def get_users(current_user: SchemaUser = Depends(get_current_user)):
    users = db.session.query(ModelUser).all()
    return users



# Start the application
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
