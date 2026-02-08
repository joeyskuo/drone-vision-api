from fastapi import FastAPI
from routers import object_detect

app = FastAPI()
app.include_router(object_detect.router)

@app.get('/')
def index():
    return {"status": "ok"}