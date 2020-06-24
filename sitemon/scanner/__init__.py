import yaml

from sitemon.kafka import Producer

from .scanner import Scanner
from .config import Config

async def run(config_path: str):
    with open(config_path) as fp:
        data = yaml.load(fp)
        config = Config.from_dict(data)

    async with Producer.start(config.kafka.topic, config.kafka.server) as prod:
        scanner = Scanner(prod)
        await scanner.start(config.sites, config.interval)