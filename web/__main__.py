import contextlib
from os import getenv

from fastapi import FastAPI
from faststream.rabbit import RabbitBroker
from starlette.requests import Request
from starlette.responses import Response

broker_url = getenv("BROKER_URL")
topic = getenv("TOPIC")
broker = RabbitBroker(url=broker_url)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    await broker.start()
    yield
    await broker.close()


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def logger(request: Request, handler):
    response: Response = await handler(request)
    await broker.publish(
        message={
            "url": f"{request.url}",
            "method": request.method,
            "status": response.status_code
        },
        queue=topic
    )
    return response


@app.get("/")
async def index():
    return {"status": "OK"}


@app.get("/contact")
async def contact():
    return {"status": "OK"}


if __name__ == '__main__':
    from uvicorn import run
    run(app=app, host="0.0.0.0", port=8000)
