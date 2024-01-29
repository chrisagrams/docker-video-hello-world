from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from models import Base, User


app = FastAPI()

DATABASE_URL = "sqlite:///./db/test.db"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/create_user/{name}")
async def create_user(name: str):
    try:
        with SessionLocal() as session:
            user = User(name=name)
            session.add(user)
            session.commit()
            session.close()
            return {"message": f"User {name} created"}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database Error")


@app.get("/user/{name}")
async def get_user(name: str):
    try:
        with SessionLocal() as session:
            user = session.query(User).filter(User.name == name).first()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return user
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database Error")
