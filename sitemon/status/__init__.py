import yaml
from .config import Config
from .status import run_worker


async def run(config_path: str):
    with open(config_path) as fp:
        data = yaml.load(fp)
        config = Config.from_dict(data)

    await run_worker(config.kafka)
