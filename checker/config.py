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


