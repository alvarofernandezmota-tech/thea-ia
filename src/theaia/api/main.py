from fastapi import FastAPI

app = FastAPI(title="Thea IA API", version="1.0.0")

@app.get("/")
async def root():
    return {"status": "Thea IA API running successfully"}
