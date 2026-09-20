from pydantic import BaseModel, Field


class SettingsUpdate(BaseModel):
    # 必须为正数；0、负数、非数字由 pydantic 拒绝（422），不会触达写库
    slow_fee_cap: float = Field(gt=0)
