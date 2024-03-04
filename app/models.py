#%%
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime

# Base class for models
Base = declarative_base()

    
class Pain(Base):
    """
    SQLAlchemy model for the 'pain' table.

    Attributes:
        id (int): primary key of the pain entry.
        date_time (datetime): datetime of the pain entry.
        pain_level (int): level of pain.

    Methods:
        __repr__: Returns a string representation of the pain entry.
    """

    __tablename__ = "pain"

    id                  = Column(Integer, primary_key=True, index=True)
    date_time           = Column(DateTime, index=True, default=datetime.now())
    pain_level          = Column(Integer, nullable=False, index=True)

    def __repr__(self):
        return f"""<pain(
        date_time={self.date_time}, 
        pain_level={self.pain_level})>"""
    



#%%