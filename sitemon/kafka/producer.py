from contextlib import asynccontextmanager
from aiokafka import AIOKafkaProducer

import asyncio
import sys
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
        for i in range(9, -1, -1):
            try:
                prod = AIOKafkaProducer(bootstrap_servers=server)
            except:
                if not i:
                    raise
                print('Waiting for Kafka...', file=sys.stderr)
                await asyncio.sleep(3)
            else:
                break

        try:
            await prod.start()
            yield cls(topic, prod)
        finally:
            await prod.stop()

