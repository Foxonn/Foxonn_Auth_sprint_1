from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

__all__ = ['EventModel']


class EventInfoModel(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class EventModel(BaseModel):
    info: EventInfoModel = Field(default=EventInfoModel())
