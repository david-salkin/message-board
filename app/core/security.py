from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.cfg import cfg_settings

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.cfg import cfg_settings
from app.db.database import get_db_session
from app.db.model import User
from app.svc import users as user_service
from pydantic import BaseModel
from typing import Optional

SECRET_KEY = cfg_settings.SECRET_KEY
ALGORITHM = cfg_settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # tells FastAPI to look for the token at the /login endpoint
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__truncate_error=False)  # truncate password but sdon't crash

"""
Note on Swagger UI (http://localhost:8000/docs): the Authorize button targets the `/login route using standard OAuth2 Form data. 
FastAPI validates the credentials against the hashed database entry, generates a JWT, and passes it back to Swagger which
then places this token in browser memory, which unlocks the padlock icons next to the endpoints.
"""
class TokenData(BaseModel):
	sub: str  # ignore all other fields in the token because only sub is required


def get_hash_password(password: str) -> str:
	return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
	return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db_session)) -> User:
	
	try:
		payload = jwt.decode(token, cfg_settings.SECRET_KEY, algorithms=[cfg_settings.ALGORITHM])
		token_data = TokenData(**payload)  # validate sub and ignore everything else
		username = token_data.sub
		
		if not isinstance(username, str):
			raise HTTPException(status_code=401, detail="Invalid token subject")
			
	except JWTError as e:
		raise HTTPException(status_code=401, detail=f"Could not validate credentials: {e}")

	user = await user_service.get_user_by_username(session, username)

	if not user:
		raise HTTPException(status_code=401, detail="User not found")
	
	return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
	
	to_encode = data.copy()
	
	if expires_delta:
		expire = datetime.now(timezone.utc) + expires_delta
	else:
		expire = datetime.now(timezone.utc) + timedelta(minutes=15)
	
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, cfg_settings.SECRET_KEY, algorithm=cfg_settings.ALGORITHM)
	
	return encoded_jwt