from fastapi import APIRouter
from app.schemas.settings import SettingsUpdate
from app.services.taxi_service import TaxiService
router = APIRouter()
@router.get("/settings")
def settings():
    with TaxiService() as s: return s.settings_normalized()
@router.put("/settings")
def update_settings(body: SettingsUpdate):
    with TaxiService() as s: return s.save_settings_slow_cap(body.slow_fee_cap)
