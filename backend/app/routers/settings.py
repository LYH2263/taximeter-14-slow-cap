from fastapi import APIRouter, HTTPException
from app.schemas.settings import SlowFeeCapUpdate
from app.services.taxi_service import TaxiService
router = APIRouter()
@router.get("/settings")
def settings():
    with TaxiService() as s: return s.settings()
@router.put("/settings/slow-fee-cap")
def put_slow_fee_cap(body: SlowFeeCapUpdate):
    with TaxiService() as s:
        try:
            cap = s.update_slow_fee_cap(body.slow_fee_cap)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"slow_fee_cap": cap}
