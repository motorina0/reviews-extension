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
from .crud import (
    create_survey,
    create_survey_item,
    delete_survey,
    delete_survey_item,
    get_survey_items,
    get_surveys,
)
from .models import PartialSurvey, PartialSurveyItem, Survey, SurveyItem


@reviews_ext.post("/api/v1/survey")
async def api_create_survey(data: PartialSurvey, wallet: WalletTypeInfo = Depends(require_admin_key)) -> Survey:
    
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


@reviews_ext.post("/api/v1/survey/item")
async def api_create_survey_item(data: PartialSurveyItem, wallet: WalletTypeInfo = Depends(require_admin_key)) -> SurveyItem:
    try:
       return await create_survey_item(wallet.wallet.user, data)
    except Exception as ex:
        logger.warning(ex)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Cannot create survey",
        )


@reviews_ext.get("/api/v1/survey/item/{survey_id}")
async def api_get_survey_items(survey_id:str, wallet: WalletTypeInfo = Depends(require_invoice_key)) -> List[SurveyItem]:
    try:
        return await get_survey_items(wallet.wallet.user, survey_id)
    except Exception as ex:
        logger.warning(ex)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Cannot fetch surveys",
        )

@reviews_ext.delete("/api/v1/survey/item/{survey_item_id}")
async def api_delete_survey_item(survey_item_id: str, wallet: WalletTypeInfo = Depends(require_admin_key)):
    try:
        await delete_survey_item(wallet.wallet.user, survey_item_id)
    except Exception as ex:
        logger.warning(ex)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Cannot delete survey",
        )