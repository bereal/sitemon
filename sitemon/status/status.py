from sitemon.kafka import Consumer
from .config import KafkaConfig


async def run_worker(config: KafkaConfig):
    async with Consumer.start('sitemon-status', config.topic, config.server) as consumer:
        while True:
            async with consumer.fetch_report() as report:
                print(report)