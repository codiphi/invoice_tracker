from pydantic import BaseModel
from typing import Optional

class MonthRequest(BaseModel):
    month: int
    year: Optional[int] = None