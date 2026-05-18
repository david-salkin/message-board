from pyexpat.errors import messages

from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, InstrumentedAttribute
from app.db.model import MessageCreateRequest, Message, MessageReadResponse, MessageUserResponse, UserPublic
from typing import cast


async def create_message(session: AsyncSession, msg_req: MessageCreateRequest, user_id: int) -> Message:
	"""
		Accepts the Data Transfer Object and the user_id which was extracted by the router.
	"""
	db_message = Message(content=msg_req.content, user_id=user_id) # map DTO to the Database Entity

	session.add(db_message)
	await session.commit()
	await session.refresh(db_message)
	
	return db_message


async def get_all_messages(session: AsyncSession) -> list[MessageReadResponse]:
	
	# joinedload(Message.author) causes SQLAlchemy vs. Pylance war
	# Pylance statically sees author: User but it is really author: InstrumentedAttribute
	statement = select(Message).options(joinedload(cast(InstrumentedAttribute, Message.author)))
	rv = await session.execute(statement)
	
	# responses contains a  list of Message Database Objects.
	# Each one has a property called .author which contains a full User Database Object.
	responses = list(rv.scalars().all())  # TODO: remove list() and test
	messages: list[MessageReadResponse] = []

	for resp in responses:
		# asserts silence Pylance
		assert resp.id is not None
		assert resp.author is not None

		messages.append(
			MessageReadResponse(
				id=resp.id,
				content=resp.content,
				upvotes=resp.upvotes,
				timestamp=resp.timestamp,
				author=UserPublic.model_validate(resp.author),
			)
		)

	return messages


async def get_user_messages(session: AsyncSession, user_id: int) -> list[MessageUserResponse]:
	
	statement = (
		select(Message)
		.options(joinedload(cast(InstrumentedAttribute, Message.author)))
		.where(Message.user_id == user_id))
	rv = await session.execute(statement)
	
	responses = rv.scalars().all()
	messages: list[MessageUserResponse] = []

	for m in responses:
		assert m.id is not None
		assert m.author is not None

		messages.append(
			MessageUserResponse(
				id=m.id,
				content=m.content,
				timestamp=m.timestamp,
				author=UserPublic.model_validate(m.author),
			)
		)

	return messages

async def delete_user_message(session: AsyncSession, message_id: int, user_id: int):
	
	# Matches both the id and the owner
	statement = select(Message).where((Message.id == message_id), (Message.user_id == user_id))
	result = await session.execute(statement)
	message = result.scalar_one_or_none()

	if not message:
		raise HTTPException(status_code=403, detail="Message not found")

	await session.delete(message)
	await session.commit()


async def process_vote(session: AsyncSession, message_id: int, is_upvote: bool) -> Message:

	statement = select(Message).where(Message.id == message_id)
	result = await session.execute(statement)
	message = result.scalar_one_or_none()

	if message is None:
		raise HTTPException(status_code=404, detail="Message not found")

	message.upvotes += 1 if is_upvote else -1

	session.add(message)
	await session.commit()
	await session.refresh(message)

	return message
