from enum import Enum
from pydantic import BaseModel

class ReactionType(str, Enum):
    like = "like"
    dislike = "dislike"

class ReactionRequest(BaseModel):
    reaction_type: ReactionType
