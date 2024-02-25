#%%
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import routes
from database import init_db, InitDBIn
import models
from utils.parameters import SQLALCHEMY_DATABASE_URL

app = FastAPI()

#init db
init_params = InitDBIn(url=SQLALCHEMY_DATABASE_URL, base=models.Base)
_, _ = init_db(init_params)


#include API routes
app.include_router(routes.router)#, prefix="/api")