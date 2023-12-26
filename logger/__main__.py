from http import HTTPMethod, HTTPStatus
from os import getenv

from faststream import FastStream
from faststream.rabbit import RabbitBroker
from pydantic import BaseModel


class Log(BaseModel):
    url: str
    method: HTTPMethod
    status: HTTPStatus


broker_url = getenv("BROKER_URL")
topic = getenv("TOPIC")


broker = RabbitBroker(url=broker_url)
app = FastStream(broker=broker)


@broker.subscriber(topic)
async def logger(log: Log):
    print(log)


if __name__ == '__main__':
    from asyncio import run
    run(app.run())
