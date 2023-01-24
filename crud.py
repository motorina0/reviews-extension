import json
from typing import List, Optional

from lnbits.helpers import urlsafe_short_hash

from . import db
from .models import PartialSurvey, PartialSurveyItem, Survey, SurveyItem


########################## SURVEYS ####################
async def create_survey(user_id: str, data: PartialSurvey) -> Survey:
    survey_id = urlsafe_short_hash()
    meta = data.dict()

    await db.execute(
        """
        INSERT INTO reviews.surveys (
            id,
            "user",
            meta
        )
        VALUES (?, ?, ?)
        """,
        (
            survey_id,
            user_id,
            json.dumps(meta)
        ),
    )
    survey = await get_survey(user_id, survey_id)
    assert survey, "Created survey cannot be retrieved"
    return survey


async def get_survey(user_id: str, survey_id: str) -> Optional[Survey]:
    row = await db.fetchone("""SELECT * FROM reviews.surveys WHERE "user" = ? AND id = ?""", (user_id, survey_id,))

    return Survey.parse_obj({"id": row["id"], **json.loads(row["meta"])}) if row else None

async def get_surveys(user_id: str) -> List[Survey]:
    rows = await db.fetchall("""SELECT * FROM reviews.surveys WHERE "user" = ?""", (user_id,))

    return [Survey.parse_obj({"id": row["id"], **json.loads(row["meta"])}) for row in rows]

async def delete_survey(user_id: str, survey_id: str):
   await db.execute("""DELETE FROM reviews.surveys WHERE "user" = ? AND id = ?""", (user_id, survey_id,))


########################## SURVEY ITEMS ####################

async def create_survey_item(user_id: str, data: PartialSurveyItem) -> SurveyItem:
    survey_item_id = urlsafe_short_hash()
    meta = data.dict()

    await db.execute(
        """
        INSERT INTO reviews.survey_items ( "user",  id,  survey_id, meta)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            survey_item_id,
            data.survey_id,
            json.dumps(meta)
        ),
    )
    survey_item = await get_survey_item(user_id, survey_item_id,)
    assert survey_item, "Created survey_item item cannot be retrieved"
    return survey_item


async def get_survey_item(user_id: str, survey_item_id: str) -> Optional[SurveyItem]:
    row = await db.fetchone("""SELECT * FROM reviews.survey_items WHERE "user" = ? AND id = ?""", (user_id, survey_item_id,))

    return SurveyItem.parse_obj({"id": row["id"], "survey_id": row["survey_id"], **json.loads(row["meta"])}) if row else None

async def get_survey_items(user_id: str, survey_id: str) -> List[SurveyItem]:
    rows = await db.fetchall("""SELECT * FROM reviews.survey_items WHERE "user" = ? AND survey_id = ?""", (user_id, survey_id,))

    return [SurveyItem.parse_obj({"id": row["id"], "survey_id": row["survey_id"], **json.loads(row["meta"])}) for row in rows]

async def delete_survey_item(user_id: str, survey_item_id: str):
   await db.execute("""DELETE FROM reviews.survey_items WHERE "user" = ? AND id = ?""", (user_id, survey_item_id,))

