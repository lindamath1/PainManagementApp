#%%
from datetime import datetime
from pydantic import BaseModel, conint
from typing import Optional

class PainCreate(BaseModel):
  """Pydantic model for creating Pain"""
  date_time: Optional[datetime] = None
  pain_level: int#conint(ge=0, le=10)

class PainInDB(PainCreate):
  """Pain ORM model"""
  id: int
  is_active: bool = True



#%%