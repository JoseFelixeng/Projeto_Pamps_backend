"""Database connection"""
from .config import settings
from fastapi import Depends
from sqlmodel import Session, create_engine

engine = create_engine(
    settings.db.uri,
    echo=settings.db.echo,
    connect_args=settings.db.connect_args,
)

#Criando uma dependia usavel
def get_session():
    with Session(engine) as session:
        yield session

    
ActiveSession = Depends(get_session)