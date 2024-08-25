import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.db.config import settings
from app.db.database import sessionmanager
from app.routes import well_declines

from app.db.utils import create_db_and_tables

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.triangolo.com/advanced/events/
    """
    # Load and ML model or something else shared once that can take a while
    await create_db_and_tables(sessionmanager)
    yield
    # Clean up and release resources
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(
    lifespan=lifespan,
    title="Base Generic API",
    description=settings.PROJECT_NAME,
    docs_url="/"
)

# all origins. Put in your domains when they are setup
# to only allow api calls from them
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(well_declines.router)


