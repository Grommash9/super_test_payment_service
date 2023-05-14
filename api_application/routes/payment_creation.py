import re
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi_limiter.depends import RateLimiter
from pydantic.class_validators import validator
from pydantic.main import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse
from api_application import config
import uuid
from local_extension import db_methods

formatted_router = APIRouter()
token_auth_scheme = HTTPBearer()


class NumberInformation(BaseModel):
    amount: str
    currency: str
    callback_url: Optional[str]

    @validator('amount')
    def bigger_than(cls, amount):
        try:
            if float(amount) <= 10:
                raise ValueError('The amount should be bigger than 10 or equal to')
        except Exception as e:
            raise ValueError(f'Amount value error: {str(e)}')
        return amount

    @validator('currency')
    def cur_codes(cls, currency):
        allowed_cur_list = ['UAH', 'USD', 'GBP', 'PLN']
        if currency not in allowed_cur_list:
            raise ValueError(f'Please use currency from the list only {allowed_cur_list}')
        return currency


@formatted_router.post('/payment', tags=['Створення виплати'], dependencies=[Depends(RateLimiter(seconds=1))])
async def create_new_payment(payout: NumberInformation, request: Request, token: str = Depends(token_auth_scheme)):
    if token.credentials != '$HIG#IRHRF#gn3ljpgHEIROF42IGHPOWJF':
        raise HTTPException(401, detail='Please check the entry of the api key in the Authorization header ')

    new_uuid = re.sub('-', '', str(uuid.uuid4()))

    await db_methods.admin_panel_payment.create_new(new_uuid, payout.amount, payout.currency,
                                                    payout.callback_url)

    return JSONResponse(content={'message': 'ok', 'payment_id': new_uuid, 'payment_url': f"{config.CSRF_TRUSTED_ORIGINS[0]}/payment_get/{new_uuid}"},
        media_type="application/json")



