from pydantic import BaseModel
from uuid import UUID


class IdSchema(BaseModel):
    id: UUID
