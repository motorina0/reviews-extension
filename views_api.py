from asyncio.log import logger
from http import HTTPStatus
from typing import List

from fastapi import Depends
from fastapi.exceptions import HTTPException

from lnbits.decorators import (
    WalletTypeInfo,
    check_admin,
    get_key_type,
    require_admin_key,
    require_invoice_key,
)

from . import reviews_ext
from .crud import create_survey, delete_survey, get_surveys
from .models import CreateSurvey, Survey


@reviews_ext.post("/api/v1/survey")
async def api_create_survey(data: CreateSurvey, wallet: WalletTypeInfo = Depends(require_admin_key)) -> Survey:
    
    try:
        survey = await create_survey(wallet.wallet.user, data)
        return survey

    except Exception as ex:
        logger.warning(ex)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Cannot create survey",
        )


@reviews_ext.get("/api/v1/survey")
async def api_get_surveys( wallet: WalletTypeInfo = Depends(require_invoice_key)) -> List[Survey]:
    try:
        return await get_surveys(wallet.wallet.user)
    except Exception as ex:
        logger.warning(ex)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Cannot fetch surveys",
        )

@reviews_ext.delete("/api/v1/survey/{survey_id}")
async def api_delete_survey(survey_id: str, wallet: WalletTypeInfo = Depends(require_admin_key)):
    try:
        await delete_survey(wallet.wallet.user, survey_id)
    except Exception as ex:
        logger.warning(ex)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Cannot delete survey",
        )