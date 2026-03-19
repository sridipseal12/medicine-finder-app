from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Medicine Finder API running"}