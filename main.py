#Python
from typing import Optional
from enum import Enum # Crear enumeraciones

#Pydantic
from pydantic import BaseModel
from pydantic import Field, EmailStr


#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File


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
@app.post("/person/new",response_model=PersonOut, status_code=status.HTTP_201_CREATED, tags=['Persons'])
def create_person(person: Person = Body(...)):
	return person

# Validaciones: Query Parameters

@app.get("/person/detail", status_code=status.HTTP_200_OK, tags=['Persons'])
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
persons = [1, 2, 3, 4, 5]

@app.get("/person/detail/{person_id}", tags=['Persons'])
def show_person(
	person_id: int = Path(
		..., 
		gt=0,
		title="Id Person",
		description="This is the id of the person",
		example=123
		)
):
	if person_id not in persons:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail= "¡This person doesn't exist!"
		)
	return {person_id: "It exists:!"}


# Validaciones: Request body

@app.put("/person/{person_id}", tags=['Persons'])
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


@app.post("/login", response_model=LoginOut, status_code=status.HTTP_200_OK, tags=['Persons'])
def login(username: str = Form(...), password: str = Form(...)):
	return LoginOut(username=username)


# Cookies and Headers Parameters
@app.post("/contact", status_code=status.HTTP_200_OK)
def contact(
	frist_name: str = Form(
		..., 
		max_length=20, 
		min_length=1), 
	last_name: str = Form(
		..., 
		max_length=20, 
		min_length=1), 
	email: EmailStr = Form(...),
	message: str = Form(
		...,
		min_length=20
		),
	user_agent: Optional[str] = Header(default=None),
	ads: Optional[str] = Cookie(default=None)

	):
		return user_agent


# Files

@app.post(
	path="/post-image"
	)
def post_image(image: UploadFile = File(...)):

	return {
		"Filename": image.filename,
		"Format": image.content_type,
		"Size(kb)":  round(len(image.file.read())/1024, ndigits=2) #obtener en kb
	}

