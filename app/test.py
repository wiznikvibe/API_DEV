from fastapi import FastAPI , Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import mysql.connector as conn
from sqlalchemy.orm import Session
from configparser import ConfigParser
import time
from app import models, schemas, utils
from app.database import engine, get_db
from app.routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

config = ConfigParser()
config.read('config.ini')

host = config['USER']['host']
admin = config['USER']['user']
password = config['USER']['password']
database = config['USER']['database']


while True:
    try:
        mydb = conn.connect(host=host, user=admin, password=password, database=database)
        cursor = mydb.cursor(buffered=True, dictionary=True)
        # tables = cursor.execute("""SHOW TABLES;""")
        print("Connection Succefully Established")
        # print(tables)
        break
    except Exception as e:
        print("Connection Failed")
        print("Error:", e)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)



@app.get("/")
def root():
    return {"message":"Hello World !"}






