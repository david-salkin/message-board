from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime, timezone

# ---------- User ----------
class User(SQLModel, table=True):
	# columns
	id: int = Field(default=None, primary_key=True)
	username: str = Field(index=True, unique=True)
	hashed_password: str
	# messages field links to Message, and Message should have a field called author
	messages: list["Message"] = Relationship(back_populates="author")


class UserCreate(SQLModel):
	# Ensure that plain text pwd never gets beyond the tx stage
	username: str
	password: str

class UserUpdate(SQLModel):
	title: Optional[str] = None
	content: Optional[str] = None

"""
Base: common fields
Actions: (e.g. MessageCreate) used as parameters in POST's
Table: Base plus additions
"""
class MessageBase(SQLModel):
	content: str
	user_id: int = Field(foreign_key="user.id")  # table user, col id must already exist

class MessageCreate(MessageBase):
	pass  # No extra fields required from ther api client

class Message(MessageBase, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) # runs the function fresh every time
	# author field links to User, and User should have a list called messages
	author: "User" = Relationship(back_populates="messages")  # links to User and enables message.user.username

class Token(SQLModel):
	access_token: str
	token_type: str = "bearer"