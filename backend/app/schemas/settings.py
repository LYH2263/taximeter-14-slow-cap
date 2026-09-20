from pydantic import BaseModel, Field

class SlowFeeCapUpdate(BaseModel):
    slow_fee_cap: float = Field(gt=0, allow_inf_nan=False)
