from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = FastAPI(title="Petshop API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class PetCreate(BaseModel):
    nome: str
    especie: str
    tutor: str

class Pet(BaseModel):
    id: int
    nome: str
    especie: str
    tutor: str
    criado_em: datetime

class ServicoCreate(BaseModel):
    descricao: str

class Servico(BaseModel):
    id: int
    pet_id: int
    descricao: str
    data: datetime

# Database connection
def get_db():
    conn = psycopg2.connect(
        os.getenv("DATABASE_URL"),
        cursor_factory=RealDictCursor
    )
    try:
        yield conn
    finally:
        conn.close()

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Pets endpoints
@app.get("/pets", response_model=List[Pet])
def listar_pets(busca: Optional[str] = None, especie: Optional[str] = None, conn=Depends(get_db)):
    cursor = conn.cursor()
    
    query = "SELECT * FROM pets WHERE 1=1"
    params = []
    
    if busca:
        query += " AND nome ILIKE %s"
        params.append(f"%{busca}%")
    
    if especie:
        query += " AND especie = %s"
        params.append(especie)
    
    query += " ORDER BY criado_em DESC"
    
    cursor.execute(query, params)
    pets = cursor.fetchall()
    cursor.close()
    
    return pets

@app.post("/pets", response_model=Pet)
def criar_pet(pet: PetCreate, conn=Depends(get_db)):
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO pets (nome, especie, tutor) VALUES (%s, %s, %s) RETURNING *",
        (pet.nome, pet.especie, pet.tutor)
    )
    
    novo_pet = cursor.fetchone()
    conn.commit()
    cursor.close()
    
    return novo_pet

@app.delete("/pets/{pet_id}")
def excluir_pet(pet_id: int, conn=Depends(get_db)):
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM pets WHERE id = %s", (pet_id,))
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    
    conn.commit()
    cursor.close()
    
    return {"message": "Pet excluído com sucesso"}

# Serviços endpoints
@app.post("/pets/{pet_id}/servicos", response_model=Servico)
def adicionar_servico(pet_id: int, servico: ServicoCreate, conn=Depends(get_db)):
    cursor = conn.cursor()
    
    # Verificar se pet existe
    cursor.execute("SELECT id FROM pets WHERE id = %s", (pet_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    
    cursor.execute(
        "INSERT INTO servicos (pet_id, descricao) VALUES (%s, %s) RETURNING *",
        (pet_id, servico.descricao)
    )
    
    novo_servico = cursor.fetchone()
    conn.commit()
    cursor.close()
    
    return novo_servico

@app.get("/pets/{pet_id}/servicos", response_model=List[Servico])
def listar_servicos_pet(pet_id: int, limite: int = 5, conn=Depends(get_db)):
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM servicos WHERE pet_id = %s ORDER BY data DESC LIMIT %s",
        (pet_id, limite)
    )
    
    servicos = cursor.fetchall()
    cursor.close()
    
    return servicos

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)