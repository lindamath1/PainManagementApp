#%%
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, declarative_base

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, DateTime, Sequence

# Base class for your models
Base = declarative_base()

    
class Pain(Base):
    """TherapySession model
    
    Attributes:
    -----------
    id : int 
        Primary key
    date_time : datetime
        Pain entry datetime
    pain_level : int
        Pain level between 0 and 10
    is_active : bool
        Is the therapy session active or not
    """
    __tablename__ = "pain"

    id                  = Column(Integer, primary_key=True, index=True)
    date_time           = Column(DateTime, index=True, default=datetime.now())
    pain_level          = Column(Integer, nullable=False, index=True)
    is_active           = Column(Boolean, default=True)

    def __repr__(self):
        return f"""<pain(
        date_time={self.date_time}, 
        pain_level={self.pain_level}, 
        is_active={self.is_active})>"""
    



#%%