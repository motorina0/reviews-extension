import json
from typing import List, Optional

from lnbits.helpers import urlsafe_short_hash

from . import db
from .models import CreateSurvey, Survey


async def create_survey(user_id: str, data: CreateSurvey) -> Survey:
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

async def delete_survey(user_id: str, survey_id: str):
   await db.execute("""DELETE FROM reviews.surveys WHERE "user" = ? AND id = ?""", (user_id, survey_id,))


async def get_surveys(user_id: str) -> List[Survey]:
    rows = await db.fetchall("""SELECT * FROM reviews.surveys WHERE "user" = ?""", (user_id,))

    return [Survey.parse_obj({"id": row["id"], **json.loads(row["meta"])}) for row in rows]