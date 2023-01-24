from fastapi import Depends

from lnbits.decorators import (
    WalletTypeInfo,
    check_admin,
    get_key_type,
    require_admin_key,
    require_invoice_key,
)

from . import reviews_ext
from .crud import create_survey
from .models import CreateSurvey

# add your endpoints here


@reviews_ext.post("/api/v1/survey")
async def api_create_survey(data: CreateSurvey, wallet: WalletTypeInfo = Depends(require_admin_key),):
    
    print("### data", data)
    survey = await create_survey(wallet.wallet.user, data)
    return survey

@reviews_ext.get("/api/v1/test/{test_data}")
async def api_reviews(test_data):
    # Do some python things and return the data
    return test_data
