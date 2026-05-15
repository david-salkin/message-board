from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.db.model import User, UserCreateRequest
from app.core import security, cfg

async def create_user(session: AsyncSession, user_request: UserCreateRequest) -> User:

	hashed = security.get_hash_password(user_request.password)   
	user = User(username=user_request.username, hashed_password=hashed)
	session.add(user)
	await session.commit()
	await session.refresh(user)  # reload object to get its ID
	
	return user


async def authenticate_user(session: AsyncSession, username: str, password: str) -> User | None:
	
	user = await get_user_by_username(session, username)
	
	if not user:
		return None
	
	if not security.verify_password(password, user.hashed_password):
		return None
		
	return user

async def get_user_by_username(session: AsyncSession, username: str) -> User | None:

	sql = select(User).where(User.username == username)
	result = await session.execute(sql)
	
	return result.scalar_one_or_none()


async def login_for_access_token(user: User) -> dict:
	"""
	Returns the access token dictionary.
	In JWT sub is the username which we include in the token
	"""
	access_token_expires = timedelta(minutes=cfg.cfg_settings.ACCESS_TOKEN_EXPIRE_MINUTES)    
	access_token = security.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
	
	return {"access_token": access_token, "token_type": "bearer"}
