from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SurveyType(str, Enum):
    # give a score to each item
    RATING = 'rating'
    # choose one item from a list
    POLL = 'poll',
    # like or dislike an item
    LIKES = 'likes'


class PartialSurvey(BaseModel):
   wallet: str
   type: "SurveyType"
   name: str
   amount: int # sats required to vote
   description: Optional[str]
   expiry_date: Optional[str] # ISO8601
   allow_comments = True
   show_results = True

class Survey(PartialSurvey):
   id: str



class PartialSurveyItem(BaseModel):
    survey_id: str
    name: str
    description: str

class SurveyItem(PartialSurveyItem):
    id: str
    lnurl_id: Optional[str] #todo: remove optional


class Review(BaseModel):
    item_id: str
    rating: int
    comments: Optional[str]