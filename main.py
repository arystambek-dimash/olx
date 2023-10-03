from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from config import database, settings
from app.auth.routers import router

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(**settings.fastapi_config)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.env.CORS_ORIGINS,
    allow_methods=settings.env.CORS_METHODS,
    allow_headers=settings.env.CORS_HEADERS,
    allow_credentials=True,
)

app.include_router(router, prefix="/auth", tags=["Auth"])
