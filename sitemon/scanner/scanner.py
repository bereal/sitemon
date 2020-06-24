import asyncio
import dataclasses
import re
import time
from aiokafka import AIOKafkaProducer
from typing import List, Optional

import yaml
from aiohttp import ClientSession

from sitemon.model import SiteReport, asdict
from .config import Config, SiteConfig


class Client:
    '''Abstracts away the HTTP logic
    '''
    async def get(self, url) -> str:
        async with ClientSession() as s:
            async with s.get(url) as r:
                return await r.body()


class Scanner:
    '''Main worker on the producer side
    '''

    # in a more complex case the producer logic would be extracted
    # to a separate class, but I decided this would be unnecessary here
    def __init__(self, topic: str, producer: AIOKafkaProducer, client: Client=None):
        self._topic = topic
        self._producer = producer
        self._client = client or Client()

    async def scan_site(self, url, pattern=None):
        '''Load the url and check if the pattern matches.
        Send the notification to Kafka
        '''
        report = SiteReport(url, 0)
        before = time.monotonic()
        try:
            text = await self._client.get(url)
        except Exception as ex:
            report.error = str(ex)
        else:
            if pattern:
                found = bool(re.search(pattern, text))
                report.pattern_match = found

        report.response_time = time.monotonic() - before
        await self._producer.send(self._topic, asdict(report))

    async def scan_all(self, sites: List[SiteConfig]):
        await asyncio.wait([
            self.scan_site(s.url, s.pattern) for s in sites
        ])

    async def start(self, sites: List[SiteConfig], interval: int):
        while True:
            await self.scan_all(sites)
            await asyncio.sleep(interval)


