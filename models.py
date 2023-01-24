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


class Survey(BaseModel):
   id: str
   wallet: str
   type: "SurveyType"
   name: str
   amount: int # sats required to vote
   allow_comments = True
   show_results = True
   description: Optional[str]
   lnurl_id: Optional[str]



class CreateSurvey(BaseModel):
   wallet: str
   type: "SurveyType"
   name: str
   amount: int
   description: Optional[str]

class SurveyItem(BaseModel):
    id: str
    survey_id: str
    name: str
    description: str
    lnurl_id: Optional[str]





class Review(BaseModel):
    item_id: str
    rating: int
    comments: Optional[str]