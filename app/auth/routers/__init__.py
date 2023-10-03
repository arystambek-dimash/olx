from fastapi import APIRouter
from sqlalchemy.orm import Session

from config.settings import import_routers

router = APIRouter()
import_routers(__name__)
