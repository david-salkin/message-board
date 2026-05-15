from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.database import get_db_session
from app.db.model import User, UserCreateRequest, MessageCreateRequest, MessageCreateResponse, MessageReadResponse, MessageUserResponse, VoteRequest
from app.svc import users as user_service
from app.svc import messages as message_service
from app.core import security

router = APIRouter()

# ---- Feature-level endpoints ----
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreateRequest, session: AsyncSession = Depends(get_db_session)):
	"""
	Register a new user account.
	"""
	return await user_service.create_user(session, user_in)


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db_session)):

	"""
	Log in with username and password to receive an access token.
	"""
	# Don't use UserCreateRequest SQLModel as the login info because the OAuth2 
	# specification (and FastAPI's Swagger) requires login credentials 
	# to be sent as Form Data (application/x-www-form-urlencoded). 
	
	# Pydantic/SQLModel expects JSON, which would cause an Unprocessable Entity error when 
	# clicking the 'Authorize' button in Swagger or when using standard OAuth2 client tools.

	# FastAPI looks in the form for fields username and password, and then creates the OAuth2PasswordRequestForm object.
	user = await user_service.authenticate_user(session, form_data.username, form_data.password)

	if not user:
		raise HTTPException(status_code=401, detail="Invalid credentials")
	
	return await user_service.login_for_access_token(user)
	# Now, any route you protect with get_current_user is accessible


@router.post("/messages", response_model=MessageCreateResponse, status_code=201)
async def create_message(message_request: MessageCreateRequest, session: AsyncSession = Depends(get_db_session),
							current_user: User = Depends(security.get_current_user)):
	"""
	Create a new message.
	"""
	# Extract the user id and send to business logic.
	# FastAPI filters msg to return just a MessageCreateResponse
	msg =  await message_service.create_message(session=session, msg_req=message_request, user_id=current_user.id)
	return msg


@router.get("/messages", response_model=list[MessageReadResponse])
async def get_all_messages(session: AsyncSession = Depends(get_db_session)):
	"""
	Retrieve all messages from the board.
	"""
	return await message_service.get_all_messages(session=session)

@router.get("/user/messages", response_model=list[MessageUserResponse])
async def get_user_messages(session: AsyncSession = Depends(get_db_session), current_user: User = Depends(security.get_current_user)):
	"""
	Retrieve all messages posted by the user.
	"""
	return await message_service.get_user_messages(session=session, user_id=current_user.id)


@router.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(message_id: int, 
						 session: AsyncSession = Depends(get_db_session), 
						 current_user: User = Depends(security.get_current_user)):
	"""
    Permanently delete a message owned by the user.
    """
	return await message_service.delete_user_message(session=session, message_id=message_id, user_id=current_user.id)


@router.post("/logout")
async def logout(current_user: User = Depends(security.get_current_user)):
	"""
	Logout from the current session.
	"""
	# Not a real logout
	return {"message": f"{current_user.username} successfully logged out"}


@router.post("/messages/{message_id}/vote")
async def vote_for_message(
    message_id: int,
    vote_data: VoteRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(security.get_current_user)
):
    """
    Pass upvote as {"is_upvote": true}
	Pass downvote as {"is_upvote": false}
    """
    return await message_service.process_vote(session, message_id, vote_data.is_upvote)
