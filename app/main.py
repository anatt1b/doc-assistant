from fastapi import FastAPI, UploadFile, File, HTTPException # FastAPI + tiedoston vastaanotto
from pathlib import Path # Tuodaan Path-luokka tiedostopolkujen käsittelyyn
import uuid # Tuodaan uuid-kirjasto uniikkien tunnisteiden luomiseen


app = FastAPI() # Luodaan FastAPI-sovellus

BASE_DIR = Path(__file__).resolve().parent.parent # Määritellään peruspolku, joka on tämän tiedoston sijainti
UPLOAD_DIR = BASE_DIR / "uploads" # Määritellään polku, johon ladatut tiedostot tallennetaan
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

@app.post("/ask") # Määritellään reitti /ask, joka vastaa HTTP POST -pyyntöihin
async def ask(file_id: str, question: str): # Määritellään funktio, joka ottaa vastaan tiedoston tunnisteen ja kysymyksen
    matches = list(UPLOAD_DIR.glob(f"{file_id}_*"))# Määritellään polku, josta tiedosto haetaan
    if not matches: # Tarkistetaan, että tiedosto löytyy
        raise HTTPException(status_code=404, detail="File not found") # Jos tiedostoa ei löydy, palautetaan 404-virhe   
    file_path = matches[0] # Oletetaan, että tiedosto löytyy ja otetaan ensimmäinen osuma   
    text = file_path.read_text(errors="ignore") # Luetaan tiedoston sisältö tekstinä, ohittaen mahdolliset virheet

    # TODO: TÄHÄN KOHTAAN VAIHDETAAN OPENAI-LOGIIKKA
    # Nyt oalautetaan vain osa tiedostosta testimielessä
    # Myöhemmin tässä kohdassa:
    # 1) Lähetetään 'text' +'question' OpenAI:lle
    # 2) Saadaan OpenAI:lta vastaus, joka palautetaan käyttäjälle
    
    return {"question": question, "preview": text[:500]}  # MVP-vastaus
