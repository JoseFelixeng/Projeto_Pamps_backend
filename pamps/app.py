from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routes import main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialização de recursos globais pode vir aqui
    yield
    # Encerramento de recursos aqui


app = FastAPI(
    title="Pamps",
    version="0.1.0",
    description="Pamps is a posting app",
    lifespan=lifespan,
)

app.include_router(main_router)
