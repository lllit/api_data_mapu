import json
import os
from typing import Any
from datetime import timedelta
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from utils.security import create_access_token, get_current_user

from contextlib import asynccontextmanager

from dotenv import load_dotenv

from pydantic import BaseModel

from Models.model_token import Token


load_dotenv()


ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))



app = FastAPI()



USERNAME_API = os.getenv("USER_API")
PASSWORD_API = os.getenv("PASSWORD_API")



# ---- INICIO ------
@app.get("/", tags=["Inicio"])
def saludo():
    return {"Bienvenido a la api": ""}



#-------- TOKEN ----------
@app.post("/token", response_model=Token, tags=["Login"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Aquí deberías validar el usuario y la contraseña
    # Este es un ejemplo simple que acepta cualquier usuario y contraseña
    if form_data.username != USERNAME_API or form_data.password != PASSWORD_API:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ------- MAPU API -------
@app.get(
    path="/get_data_mapu",
    name="Obtener Informacion Mapuche",
    description="Returns the data from the MapuFiles JSON file.",
    tags=["Mapu Data ALL"]     
)
def get_data_mapu():
    try:
        # Ruta al archivo JSON
        json_path = Path("brain_mapu/json_data/mapuche_data.json")

        # Verifica si el archivo existe
        if not json_path.exists():
            return {"error": "El archivo JSON no existe."}

        # Lee el archivo JSON
        with json_path.open("r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            
        # Crear el payload para enviar a la API
        payload_dict = data
        
        return payload_dict
    
    except Exception as e:
        print("Error: ",e)



@app.get(
    path="/get_data_mapu_selected",
    name="Obtener Informacion Mapuche",
    description="Returns the data from the Selected MapuFiles JSON file.",
    tags=["Mapu Data Selected"] 
)
def get_data_mapu_selected():
    try:
        # Ruta al archivo JSON
        json_path = Path("brain_mapu/json_data/mapuche_data_selected.json")

        # Verifica si el archivo existe
        if not json_path.exists():
            return {"error": "El archivo JSON no existe."}

        # Lee el archivo JSON
        with json_path.open("r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        # Crear el payload para enviar a la API
        payload_dict = data
        
        return payload_dict

    except Exception as e:
        print(e)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=3300)