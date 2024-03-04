#%%
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field

class PainCreate(BaseModel):
    """
    Input model to create Pain.

    Attributes:
        date_time (Optional[datetime]): datetime of the pain entry.
        pain_level (Annotated[int, Field(ge=0, le=10)]): level of pain recorded.
    """
    date_time: Optional[datetime] = None
    pain_level: Annotated[int, Field(ge=0, le=10)]

class PainInDB(PainCreate):
    """
    Database model for Pain entries.

    Args:
        id (int): primary key of the pain entry in the database.
    """
    id: int


#%%