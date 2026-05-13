from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.model import MessageCreate, Message

async def create_message(session: AsyncSession, message_in: MessageCreate, author_id: int) -> Message:

	db_message = Message(content=message_in.content, user_id=author_id)  # id from JWT
	# This links it to the User.id we just discussed
	
	session.add(db_message)
	await session.commit()
	await session.refresh(db_message)
	
	return db_message