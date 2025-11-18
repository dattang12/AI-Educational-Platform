from fastapi import FastAPI
from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.routers import content, auth, users

app = FastAPI(title="AI Educational Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(content.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "server running"}


