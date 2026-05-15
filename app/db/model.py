from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel

# ---------- User ----------
class UserCreateRequest(SQLModel):
	"""
		The Data Transfer Object.
		To ensure that plain text pwd never gets beyond the tx stage,
		It will be converted to the DB entity: User
	"""
	username: str
	password: str


class User(SQLModel, table=True):
	"""
		DB entity.
		messages links to Message, and Message has a field called author
	"""
	id: int = Field(default=None, primary_key=True)
	username: str = Field(index=True, unique=True)
	hashed_password: str
	messages: list["Message"] = Relationship(back_populates="author")


class MessageBase(SQLModel):
	"""
		Common fields.
		e.g. {"content": "This board is really going south!"}
		Removed: user_id as client shouldn't send it ensuring that the person 
		writing the message is actually the person logged in.
	"""
	content: str
	

class MessageCreateRequest(MessageBase):
	# The DTO
	pass  # No extra fields required from api client


class Message(MessageBase, table=True):
	"""
		The DB entity.

		The author field links to User, and User has a list called messages.
		A Relationship is an object.
		The id field is okay to be empty (Optional) before DB sets it and unrequired in constructor (default=None)
	"""
	id: Optional[int] = Field(default=None, primary_key=True)
	timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) # lambda refreshes each time
	
	user_id: int = Field(foreign_key="user.id")  # set in the service layer
	upvotes: int = Field(default=0)
	author: "User" = Relationship(back_populates="messages")  # links to User and enables message.user.username


class MessageCreateResponse(SQLModel):
	"""
		Send minimal info back to the client
	"""
	id: int
	timestamp: datetime

class UserPublic(SQLModel):
	"""
		FASTapi sees MessageReadResponse wants a UserPublic object for the author. 
		Since the User database object has a 'username' field that matches the UserPublic field, 
		it morphs (instantiates) a UserPublic instance using the data from the User database object.
	"""
	username: str 


class MessageReadResponse(SQLModel):
	# includes votes
	id: int
	content: str
	upvotes: int
	timestamp: datetime
	author: UserPublic

	# This fixes the SQLModel/Pydantic war
	# Message ORM object can build MessageReadResponse
	# Pylance would compain about messages: list[MessageReadResponse]
	class Config:
		from_attributes = True

class MessageUserResponse(SQLModel):
	# No votes returned
	id: int
	content: str
	timestamp: datetime
	author: UserPublic

	class Config:
		from_attributes = True

class VoteRequest(SQLModel):

    is_upvote: bool  # True == upvote, False == downvote
