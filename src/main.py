import logging
import sys
from pathlib import Path

import asyncio
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.responses import JSONResponse

sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)

from src.api.dependencies import get_db
from src.init import redis_manager
from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images


async def send_emails_bookings_today_checkin():
    async for db in get_db():
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


async def run_send_email_regularly():
    while True:
        await send_emails_bookings_today_checkin()
        await asyncio.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # asyncio.create_task(run_send_email_regularly())
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    logging.info("FastAPICache initialize")
    yield
    await redis_manager.close()


# if settings.MODE == "TEST":
#     FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_facilities)
app.include_router(router_bookings)
app.include_router(router_images)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
