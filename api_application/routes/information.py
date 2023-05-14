from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi_limiter.depends import RateLimiter
from starlette.requests import Request
from starlette.responses import JSONResponse
from local_extension import db_methods

formatted_router = APIRouter()
token_auth_scheme = HTTPBearer()


@formatted_router.get('/payment', tags=['Інформація'], dependencies=[Depends(RateLimiter(seconds=1))])
async def get_payout_status_list(request: Request, uuid: str, token: str = Depends(token_auth_scheme)):
    if token.credentials != '$HIG#IRHRF#gn3ljpgHEIROF42IGHPOWJF':
        raise HTTPException(401, detail='Please check the entry of the api key in the Authorization header ')

    payment_info = await db_methods.admin_panel_payment.get(uuid)
    return JSONResponse(content={'message': 'ok', 'payment_data': payment_info},
                        media_type="application/json")


@formatted_router.get('/status_list', tags=['Інформація'], dependencies=[Depends(RateLimiter(seconds=1))])
async def receive_callback_secret(request: Request):
    status_list = await db_methods.admin_panel_paymentstatus.get_all()
    return JSONResponse(content={
        'message': 'ok', 'status_list': status_list},
        media_type="application/json")
