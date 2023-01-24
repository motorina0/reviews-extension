import json
from typing import Optional

from lnbits.helpers import urlsafe_short_hash

from . import db
from .models import CreateSurvey, Survey


async def create_survey(user_id: str, data: CreateSurvey) -> Optional[Survey]:
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