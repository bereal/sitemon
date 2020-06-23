import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SiteConfig:
    url: str
    pattern: Optional[str] = None


@dataclass
class KafkaConfig:
    topic: str
    server: str


@dataclass
class Config:
    sites: List[SiteConfig]
    interval: int
    kafka: KafkaConfig

    @classmethod
    def from_dict(cls, d):
        return Config(
            sites=[SiteConfig(**s) for s in d.get('sites')],
            interval=d.get('interval', 10),
            kafka=KafkaConfig(**d.get('kafka')),
        )

