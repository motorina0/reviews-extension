from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class Survey(BaseModel):
   id: str
   wallet: str
   type: "SurveyType"
   allow_comments = True
   show_results = True
   lnurl_id: Optional[str]
   items: List["SurveyItem"] = []


class SurveyItem(BaseModel):
    id: str
    name: str
    description: str
    lnurl_id: Optional[str]


class SurveyType(str, Enum):
    # give a score to each item
    RATING = 'rating'
    # choose one item from a list
    POLL = 'poll',
    # like or dislike an item
    LIKES = 'likes'


class Review(BaseModel):
    item_id: str
    rating: int
    comments: Optional[str]