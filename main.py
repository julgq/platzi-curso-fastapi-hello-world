#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body

app = FastAPI()


# Models

class Person(BaseModel):
	frist_name: str
	last_name: str
	age: int 
	hair_color: Optional[str] = None
	is_married: Optional[bool] = None



@app.get("/")
def home():
	return {"Hello": "World"}

# Request and Response Body


# ... el parametro es obligatorio.
# recibe un person donde se define que es Body request entendido por FastAPI
@app.post("/person/new")
def create_person(person: Person = Body(...)):
	return person