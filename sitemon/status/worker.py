import asyncio
import yaml
from sitemon.kafka.consumer import Consumer

from .config import Config, KafkaConfig
from .persistence import Persistence

async def run_worker(config: KafkaConfig, persistence: Persistence):
    '''Run a single site report consumer in a loop
    '''
    async with Consumer.start('sitemon-status', config.topic, config.server) as consumer:
        while True:
            async with consumer.fetch_report() as report:
                await persistence.update_site_status(report)


async def run(config_path: str):
    '''A main consumer entry point
    '''
    with open(config_path) as fp:
        data = yaml.load(fp)
        config = Config.from_dict(data)

    async with Persistence.connect(config.postgres) as p:
        tasks = [
            asyncio.create_task(run_worker(config.kafka, p))
            for i in range(config.kafka.consumers)
        ]

        await asyncio.wait(tasks)
