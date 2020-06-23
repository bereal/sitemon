import yaml

from aiokafka import AIOKafkaProducer

from .scanner import Scanner
from .config import Config

async def run(config_path: str):
    with open(config_path) as fp:
        data = yaml.load(fp)
        config = Config.from_dict(data)

        producer = AIOKafkaProducer(bootstrap_servers=config.kafka.server)
        await producer.start()
        scanner = Scanner(config.kafka.topic, producer)
        await scanner.start(config.interval)