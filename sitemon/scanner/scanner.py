import asyncio
import dataclasses
import re
import time
from typing import List, Optional, Tuple

import yaml
from aiohttp import ClientSession, ClientResponseError

from sitemon.kafka import Producer, SiteReport
from .config import Config, SiteConfig


class Client:
    '''Abstracts away the HTTP logic
    '''
    async def get(self, url) -> Tuple[int, str]:
        async with ClientSession() as s:
            async with s.get(url) as r:
                return await r.status, r.body()


class Scanner:
    '''Main worker on the producer side
    '''
    def __init__(self, producer: Producer, client: Client=None):
        self._producer = producer
        self._client = client or Client()

    async def scan_site(self, url, pattern=None):
        '''Load the url and check if the pattern matches.
        Send the notification to Kafka
        '''
        report = SiteReport(url, 0)
        before = time.monotonic()
        try:
            code, text = await self._client.get(url)
        except ClientResponseError as err:
            report.response_code = err.code
            report.error_text = str(err.message)
        except Exception as ex:
            report.error_text = str(ex)
        else:
            report.response_code = code
            if pattern:
                found = bool(re.search(pattern, text))
                report.pattern = pattern
                report.pattern_match = found

        report.response_time = time.monotonic() - before
        await self._producer.send_report(report)

    async def scan_all(self, sites: List[SiteConfig]):
        await asyncio.wait([
            self.scan_site(s.url, s.pattern) for s in sites
        ])

    async def start(self, sites: List[SiteConfig], interval: int):
        while True:
            await self.scan_all(sites)
            await asyncio.sleep(interval)


