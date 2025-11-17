from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import content

app = FastAPI(title="AI Educational Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(content.router)

@app.get("/")
def root():
    return {"message": "server running"}


