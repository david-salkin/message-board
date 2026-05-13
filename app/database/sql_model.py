from sqlmodel import SQLModel, Field
from typing import Optional

# ---------- User ----------
class User(SQLModel, table=True):
    # columns
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str


# ---------- Schemas ----------
class UserCreate(SQLModel):
    username: str
    password: str

class ItemUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"