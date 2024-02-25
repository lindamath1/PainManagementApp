#%%
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from jinja2 import Environment, FileSystemLoader

import models, schemas, crud

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/pain/read", response_class=HTMLResponse)
async def get_pain_data(request : Request, db: Session = Depends(get_db)):
    print('start reading')
    pains = crud.get_pain_entries(crud.GetPainsEntriesIn(db=db))

    return templates.TemplateResponse("read/pain.html", {
        "request" : request,
        "pains": pains  
    })

@router.get("/pain/form", response_class=HTMLResponse)
async def get_pain_form(request: Request):
    default_datetime = datetime.now()
    return templates.TemplateResponse("create/pain.html", {"request": request, "edit_mode": False,  "default_pain": 0, "default_datetime": default_datetime})

@router.get("/pain/form/{pain_id}", response_class=HTMLResponse)
async def get_edit_pain_form(request: Request, pain_id: int, db: Session = Depends(get_db)):
    pain_entry = crud.get_pain_entry_by_id(crud.GetPainEntryByIdIn(db=db, pain_id=pain_id))
    default_datetime = pain_entry.date_time
    default_pain = pain_entry.pain_level
    return templates.TemplateResponse("edit/pain.html", {"request": request, "default_pain": default_pain, "edit_mode": True,  "default_datetime": default_datetime, "pain_id": pain_id})
    
    
@router.post("/pain/create/")  
async def create_pain_entry(
    request: Request,
    date_time: str = Form(...),
    pain_level: int = Form(...),
    db: Session = Depends(get_db)
):
    try:
        print("Received request to create pain entry")
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

@router.get("/")
async def home():
    print('xxxx')
    return {"message": "Welcome to my API"}

@router.get("/")
async def get_chart():
    print('xxxx')
    return {"message": "Welcome to my API"}
# #%%