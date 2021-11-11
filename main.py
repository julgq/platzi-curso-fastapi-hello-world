#Python
from typing import Optional
from enum import Enum # Crear enumeraciones

#Pydantic
from pydantic import BaseModel
from pydantic import Field, EmailStr


#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, Path, Form


app = FastAPI()


# Models

class HairColor(Enum):
	white = "white"
	brown = "brown"
	black = "Black"
	yellow = "Yellow"
	red= "Red"

class Location(BaseModel):
	city: str
	state: str
	country: str


class PersonBase(BaseModel):
	frist_name: str = Field(
		..., 
		min_length=1,
		max_length=50
		)
	last_name: str
	age: int = Field(
		...,
		gt=0,
		le=115
		)
	hair_color: Optional[HairColor] = Field(default=None)
	is_married: Optional[bool] = Field(default=None)
	email: str = EmailStr()
	

	class Config:
		schema_extra = {
			"example": {
				"frist_name": "Facundo",
				"last_name": "Garcia Martoni",
				"age": 21,
				"hair_color": "blonde",
				"is_married": False,
				"password":"hola"
			}
		}

class Person(PersonBase):
	password: str = Field(..., min_length=8)

class PersonOut(PersonBase):
	pass

class LoginOut(BaseModel):
	username: str = Field(..., max_length=20, example="miguel2021")


@app.get("/", status_code=status.HTTP_200_OK)
def home():
	return {"Hello": "World"}

# Request and Response Body
# ... el parametro es obligatorio.
# recibe un person donde se define que es Body request entendido por FastAPI
# solo devolver PersonOut para evitar regresar a la contraseña.
#@app.post("/person/new",response_model=Person,response_model_exclude={'password'})
@app.post("/person/new",response_model=PersonOut, status_code=status.HTTP_201_CREATED)
def create_person(person: Person = Body(...)):
	return person

# Validaciones: Query Parameters

@app.get("/person/detail", status_code=status.HTTP_200_OK)
def show_person(
	name: Optional[str] = Query(None, min_length=1, max_length=50, example="Rocio"),
	title="Person Name", 
	description="This is the person name. It's between 1 and 50 characters", 
	age: str = Query(
		...,
		title="Person Age",
		description="This is the person age. It's required",
		example=25
		)
):
	return {name: age}


# Validacfiones: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
	person_id: int = Path(
		..., 
		gt=0,
		title="Id Person",
		description="This is the id of the person",
		example=123
		)
):
	return {person_id: "It exists:!"}


# Validaciones: Request body

@app.put("/person/{person_id}")
def update_person(
	person_id: int = Path(
		...,
		title="Person Id",
		description="This is the person ID",
		gt=0,
		example=1
	),
	person: Person = Body(...),
	location: Location = Body(...)

):
	results = person.dict()
	results.update(location.dict())
	return results


@app.post("/login", response_model=LoginOut, status_code=status.HTTP_200_OK)
def login(username: str = Form(...), password: str = Form(...)):
	return LoginOut(username=username)