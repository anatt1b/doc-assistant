from fastapi import FastAPI, UploadFile, File # # FastAPI + tiedoston vastaanotto
from pathlib import Path # Tuodaan Path-luokka tiedostopolkujen käsittelyyn
import uuid # Tuodaan uuid-kirjasto uniikkien tunnisteiden luomiseen


app = FastAPI() # Luodaan FastAPI-sovellus

UPLOAD_DIR = Path("uploads") # Määritellään polku, johon ladatut tiedostot tallennetaan
UPLOAD_DIR.mkdir(exist_ok=True) # Luodaan kansio, jos se ei vielä ole olemassa

@app.get("/health") # Määritellään reitti /health, joka vastaa HTTP GET -pyyntöihin
def health_check():
    return {"status": "ok"} # Palautetaan JSON-objekti, joka kertoo palvelun tilan

@app.post("/upload") # Määritellään reitti /upload, joka vastaa HTTP POST -pyyntöihin
async def upload_file(file: UploadFile = File(...)): # Määritellään funktio, joka ottaa vastaan ladattavan tiedoston
    file_id = str(uuid.uuid4()) # Luodaan uniikki tunniste ladattavalle tiedostolle
    save_path = UPLOAD_DIR / f"{file_id}_{file.filename}" # Määritellään polku, johon tiedosto tallennetaan
    content = await file.read() # Luetaan ladatun tiedoston sisältö muistiin
    save_path.write_bytes(content) # Tallennetaan tiedosto levylle
    return {"file_id": file_id, "filename": file.filename} # Palautetaan JSON-objekti, joka sisältää tiedoston tunnisteen ja nimen

