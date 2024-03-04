#%%
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
import schemas
import crud
import plot
from database import get_db


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/pain/read", response_class=HTMLResponse)
async def get_pain_data(request: Request, db: Session = Depends(get_db)):
    """
    Function to retrieve pain entries from the database and render them on an HTML page.

    Args:
        request (Request): FastAPI request object.
        db (Session): SQLAlchemy database session.
    """
    print('start reading')
    pains = crud.get_pain_entries(crud.GetPainsEntriesIn(db=db))

    return templates.TemplateResponse("read/pain.html", {
        "request": request,
        "pains": pains  
    })

@router.get("/pain/form", response_class=HTMLResponse)
async def get_pain_form(request: Request):
    """
    Function to render the pain entry creation form.

    Args:
        request (Request): FastAPI request object.
    """
    default_datetime = datetime.now()
    return templates.TemplateResponse("create/pain.html", 
                                      {"request": request,
                                       "default_pain": 0,
                                       "default_datetime": default_datetime
                                       })

@router.get("/pain/form/{pain_id}", response_class=HTMLResponse)
async def get_edit_pain_form(request: Request, pain_id: int, db: Session = Depends(get_db)):
    """
    Function to render the pain entry editing form.

    Args:
        request (Request): FastAPI request object.
        pain_id (int): id of the pain entry to be edited.
        db (Session): SQLAlchemy database session.
    """
    pain_entry = crud.get_pain_entry_by_id(crud.GetPainEntryByIdIn(db=db, pain_id=pain_id))
    default_datetime = pain_entry.date_time
    default_pain = pain_entry.pain_level
    return templates.TemplateResponse("edit/pain.html", 
                                      {"request": request, 
                                       "default_pain": default_pain, 
                                       "default_datetime": default_datetime, 
                                       "pain_id": pain_id})
    
@router.post("/pain/create/")  
async def create_pain_entry(
    request: Request,
    date_time: str = Form(...),
    pain_level: int = Form(...),
    db: Session = Depends(get_db)
):
    """
    Function to create a new pain entry and render a success page.

    Args:
        request (Request): FastAPI request object.
        date_time (str): datetime of the pain entry.
        pain_level (int): level of pain recorded.
        db (Session): SQLAlchemy database session.
    """
    try:
        pain_entry = schemas.PainCreate(
            date_time=datetime.strptime(date_time, '%Y-%m-%dT%H:%M'),
            pain_level=pain_level
        )
        crud.create_pain_entry(
            crud.CreatePainEntryIn(db=db, pain_model=models.Pain, pain=pain_entry)
        )
        return templates.TemplateResponse("create/success.html", {"request": request})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@router.post("/pain/delete/{pain_id}")
async def delete_pain_entry(pain_id: int, 
                            db: Session = Depends(get_db)):
    """
    Function to delete a pain entry and return a response.

    Args:
        pain_id (int): id of the pain entry to be deleted.
        db (Session): SQLAlchemy database session.
    """
    db_pain = crud.delete_pain_entry(crud.DeletePainEntryIn(db=db, pain_id=pain_id))
    if db_pain:
        return {"message": "Pain entry deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Pain entry not found")

@router.post("/pain/edit/{pain_id}")   
async def edit_pain_entry(pain_id: int, 
                          db: Session = Depends(get_db),
                          date_time: str = Form(...),
                          pain_level: int = Form(...),):
    """
    Function to edit a pain entry and return a response.

    Args:
        pain_id (int): id of the pain entry to be edited.
        db (Session): SQLAlchemy database session.
        date_time (str): new datetime for the pain entry.
        pain_level (int): new level of pain for the pain entry.
    """
    pain_entry = schemas.PainCreate(
            date_time=datetime.strptime(date_time, '%Y-%m-%dT%H:%M'),
            pain_level=pain_level
        )
    db_pain = crud.edit_pain_entry(crud.EditPainEntryIn(pain_edited=pain_entry,
                                                        db=db, 
                                                        pain_id=pain_id))
    if db_pain:
        return {"message": "Pain entry edited successfully"}
    else:
        raise HTTPException(status_code=404, detail="Pain entry not found")

@router.get("/pain/plot", response_class=HTMLResponse)
async def get_plot(request: Request, db: Session = Depends(get_db)):
    """
    Function to retrieve pain entries, generate a plot, and render it on an HTML page.

    Args:
        request (Request): FastAPI request object.
        db (Session): SQLAlchemy database session.
    """
    pain_entries = crud.get_pain_entries(crud.GetPainsEntriesIn(db=db))
    fig_html = plot.create_plot(pain_entries=pain_entries)
    return templates.TemplateResponse("plot/pain.html", {"request": request, "plot_html": fig_html})

@router.get("/")
async def home():
    """
    Home endpoint for the API.
    """
    return {"message": "Welcome to this API"}


# #%%