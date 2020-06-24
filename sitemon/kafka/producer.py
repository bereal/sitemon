from contextlib import asynccontextmanager
from aiokafka import AIOKafkaProducer

from .schema import SiteReport, serialize_report

class Producer:
    def __init__(self, topic: str, prod: AIOKafkaProducer):
        self._topic = topic
        self._prod = prod

    async def send_report(self, report: SiteReport):
        await self._prod.send(self._topic, serialize_report(report))

    @classmethod
    @asynccontextmanager
    async def start(cls, topic: str, server: str):
        prod = AIOKafkaProducer(bootstrap_servers=server)
        try:
            await prod.start()
            yield cls(topic, prod)
        finally:
            await prod.stop()

