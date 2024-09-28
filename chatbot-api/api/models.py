from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from api.database import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(String)
    bot_response = Column(String)
    model = Column(String)
    timestamp = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    content = Column(Text)
    embedding = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


# Pydantic models for API
class ChatHistoryResponse(BaseModel):
    id: int
    user_input: str
    bot_response: str
    model: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatHistoryList(BaseModel):
    chat_history: List[ChatHistoryResponse]


class ChatInput(BaseModel):
    message: str
    model: str

    model_config = ConfigDict(from_attributes=True)


class ChatResponse(BaseModel):
    message: str

    model_config = ConfigDict(from_attributes=True)


# Add this new model
class DocumentResponse(BaseModel):
    id: int
    filename: str
    content: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


# Add this new model for the list response
class DocumentListResponse(BaseModel):
    documents: List[DocumentResponse]
