#%%
from datetime import datetime
from typing import Type
from sqlalchemy import desc
from sqlalchemy.orm import Session
from pydantic import BaseModel

from utils.parameters import SQLALCHEMY_DATABASE_URL
from database import InitDBIn, get_session
import models
import schemas

class CreatePainEntryIn(BaseModel):
    """
    Input model to create a new pain entry.
    
    Args:
        pain_model (Type[models.Pain]): SQLAlchemy model for the Pain entry.
        pain (schemas.PainCreate): pain information to be added.
        db (Session): SQLAlchemy database session.
    """
    pain_model: Type[models.Pain]
    pain: schemas.PainCreate
    db: Session

    class Config:
        arbitrary_types_allowed = True

def create_pain_entry(create_pain_in: CreatePainEntryIn):
    """
    Function to add a new pain entry to the database.
    
    Args:
        create_pain_entry (CreatePainEntryIn): pain info and db session.
    """
    db = create_pain_in.db

    if not create_pain_in.pain.date_time:
        date_time = datetime.now()
    else:
        date_time = create_pain_in.pain.date_time

    new_pain = create_pain_in.pain_model(
            date_time=date_time, 
            pain_level=create_pain_in.pain.pain_level
        )  
    db.add(new_pain)
    db.commit()

class GetPainsEntriesIn(BaseModel):
    """
    Input model to retrieve all pain entries.
    
    Args:
        db (Session): SQLAlchemy database session.
    """
    db: Session

    class Config:
        arbitrary_types_allowed = True

def get_pain_entries(get_pain_entries_in: GetPainsEntriesIn):
    """
    Function to retrieve all pain entries from the database.
    
    Args:
        get_pain_entries_in (GetPainsEntriesIn): input parameters to retrieve pain entries.
    """
    pains = (
        get_pain_entries_in.db.query(models.Pain)
        .order_by(desc(models.Pain.date_time))  # Sort by date_time in descending order
        .all()
    )
    
    return pains

class DeletePainEntryIn(BaseModel):
    """
    Input model to delete a pain entry.
    
    Args:
        db (Session): SQLAlchemy database session.
        pain_id (int): id of the pain entry to be deleted.
    """
    db: Session
    pain_id: int

    class Config:
        arbitrary_types_allowed = True

def delete_pain_entry(delete_pain_entry_in: DeletePainEntryIn):
    """
    Function to delete a pain entry from the database.
    
    Args:
        delete_pain_entry_in (DeletePainEntryIn): input parameters to delete a pain entry.
    """
    db = delete_pain_entry_in.db
    db_pain = db.query(models.Pain).filter(models.Pain.id == delete_pain_entry_in.pain_id).first()
    if db_pain:
        db.delete(db_pain)
        db.commit()
        return db_pain
    return None

class GetPainEntryByIdIn(BaseModel):
    """
    Input model to retrieve a pain entry by id.
    
    Args:
        pain_id (int): id of the pain entry to retrieve.
        db (Session): id SQLAlchemy database session.
    """
    pain_id: int
    db: Session

    class Config:
        arbitrary_types_allowed = True

def get_pain_entry_by_id(get_pain_entry_by_id_in: GetPainEntryByIdIn):
    """
    Function to retrieve a pain entry from the database by id.
    
    Args:
        get_pain_entry_by_id_in (GetPainEntryByIdIn): input parameters to retrieve a pain entry by id.
    """
    return get_pain_entry_by_id_in.db.query(models.Pain).filter(models.Pain.id == get_pain_entry_by_id_in.pain_id).first()

class EditPainEntryIn(BaseModel):
    """
    Input model to edit a pain entry.
    
    Args:
        pain_edited (schemas.PainCreate): edited pain information.
        db (Session): SQLAlchemy database session.
        pain_id (int): id of the pain entry to be edited.
    """
    pain_edited: schemas.PainCreate
    db: Session
    pain_id: int

    class Config:
        arbitrary_types_allowed = True

def edit_pain_entry(edit_pain_entry_in: EditPainEntryIn):
    """
    Function to edit a pain entry in the database.
    
    Args:
        edit_pain_entry_in (EditPainEntryIn): input parameters to edit a pain entry.
    """
    db = edit_pain_entry_in.db
    db_pain = db.query(models.Pain).filter(models.Pain.id == edit_pain_entry_in.pain_id).first()
    if db_pain:
        for key, value in edit_pain_entry_in.pain_edited.model_dump().items():
            setattr(db_pain, key, value)
        db.commit()
        return db_pain
    return None


if __name__ == "__main__":
     init_params = InitDBIn(url=SQLALCHEMY_DATABASE_URL, base=models.Base)
     session = get_session(init_params)

    #  import pandas as pd
    #  _, engine = init_db(init_params)
    #  pd.read_sql(f'SELECT * FROM pain', engine)
     pains = session.query(models.Pain).all()

     

     pain_create = schemas.PainCreate(
                            date_time=datetime(2023, 1, 15, 8, 30),
                            pain_level=10 
                            )
     create_pain_entry(CreatePainEntryIn(pain_model=models.Pain,
                                 pain=pain_create,
                                 db=session
                            ))


    #  pain_create = schemas.PainCreate(pain_level=5)
    #  create_pain_entry(CreatePainEntryIn(pain_model=models.Pain,
    #                    pain=pain_create,
    #                    db=session
    #                   ))

     pains = get_pain_entries(GetPainsEntriesIn(db=session))


    #  deleted = delete_pain_entry(DeletePainEntryIn(db=session, pain_id=3))

    #  edited = edit_pain_entry(EditPainEntryIn(pain_edited=schemas.PainCreate(
    #                                                           date_time=datetime(2023, 2, 24, 8, 30),
    #                                                           pain_level=10),
    #                                                db=session, 
    #                                                pain_id=45))

     db_pain = get_pain_entry_by_id(GetPainEntryByIdIn(pain_id=20, db=session))
     

#%%