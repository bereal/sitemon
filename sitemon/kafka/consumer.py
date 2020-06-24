from contextlib import asynccontextmanager
from aiokafka import AIOKafkaConsumer, TopicPartition

from .connect import connect
from .schema import read_report


class Consumer:
    def __init__(self, cons: AIOKafkaConsumer):
        self._cons = cons

    @asynccontextmanager
    async def fetch_report(self):
        msg = await self._cons.getone()
        tp = TopicPartition(msg.topic, msg.partition)

        site = read_report(msg.value)
        print('Received', site, flush=True)
        yield site

        await self._cons.committed(tp)

    @classmethod
    @asynccontextmanager
    async def start(cls, group: str, topic: str, server: str):
        consumer = await connect(AIOKafkaConsumer, topic, bootstrap_servers=server, group_id=group)
        try:
            await consumer.start()
            yield cls(consumer)
        finally:
            await consumer.stop()




