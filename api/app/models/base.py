#%%
from typing import Any, Optional, Dict
from datetime import date, datetime
from pydantic import BaseModel, Field, validator
from ..database import Base

from ..utils.helper import impute_time


class BaseTrackingResponse(BaseModel):
    request_timestamp: Optional[int]
    publish_timestamp: Optional[int] = Field(default=None, format="datetime")
    _impute_time = validator(
        "publish_timestamp", allow_reuse=True, pre=True, always=True
    )(impute_time)