from fastapi import FastAPI
from app.api.routes import auth
from app.db.session import engine
from app.db.base_class import Base
from app.api.routes import auth, user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
