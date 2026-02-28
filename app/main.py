from fastapi import FastAPI # Tuodaan FastAPI-luoka web-palvelinta varten

app = FastAPI() # Luodaan FastAPI-sovellus

@app.get("/health") # Määritellään reitti /health, joka vastaa HTTP GET -pyyntöihin
def health_check():
    return {"status": "ok"} # Palautetaan JSON-objekti, joka kertoo palvelun tilan