from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.database import get_db_session
from app.db.model import UserCreate, MessageCreate
from app.svc import users as user_service
from app.svc import messages as message_service

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, session: AsyncSession = Depends(get_db_session)):
	return await user_service.create_user(session, user_in)


@router.post("/login")
async def login(credentials: UserCreate, session: AsyncSession = Depends(get_db_session)):

	user = await user_service.authenticate_user(session, credentials.username, credentials.password)

	if not user:
		raise HTTPException(status_code=401, detail="Invalid credentials")
	
	return await user_service.login_for_access_token(user)
	# Now, any route you protect with get_current_user is accessible

"""
@router.post("/messages", response_model=MessageRead)
async def post_message(
	msg_in: MessageCreate, 
	session: AsyncSession = Depends(get_db_session),
	current_user = Depends(auth_service.get_current_user) # The Bouncer Guardrail
):
	return await message_service.create_post(session, msg_in, author_id=current_user.id)
"""