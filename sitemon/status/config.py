import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class PostgresConfig:
    host: str
    port: int = 5432
    user: str = 'postgres'
    password: Optional[str] = None
    db: Optional[str] = None


@dataclass
class KafkaConfig:
    topic: str
    server: str
    consumers: int = 1


@dataclass
class Config:
    consumers: int
    kafka: KafkaConfig
    postgres: PostgresConfig

    @classmethod
    def from_dict(cls, d):
        return Config(
            consumers=1,
            kafka=KafkaConfig(**d.get('kafka')),
            postgres=PostgresConfig(**d.get('postgres')),
        )

