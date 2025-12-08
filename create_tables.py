from app.core.database import Base, engine
from app.models import user_model, content_model

print("Create Tables ...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully")
