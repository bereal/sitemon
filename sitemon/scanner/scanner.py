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
        '''Load a web page, return response code and the content
        '''
        async with ClientSession() as s:
            async with s.get(url) as r:
                return r.status, await r.text()


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
            # Error returned by the web server
            report.response_code = err.code
            report.error_text = str(err.message)
        except Exception as ex:
            # Arbitrary error, e.g. network
            report.error_text = str(ex)
        else:
            report.response_code = code
            if pattern:
                found = bool(re.search(pattern, text))
                report.pattern = pattern
                report.pattern_match = found

        report.response_time = int(time.monotonic() - before)
        await self._producer.send_report(report)

    async def scan_all(self, sites: List[SiteConfig]):
        '''Check all the sites concurrently
        '''
        await asyncio.wait([
            self.scan_site(s.url, s.pattern) for s in sites
        ])

    async def start(self, sites: List[SiteConfig], interval: int):
        '''Keep checking the sites forever with the given interval
        '''
        while True:
            await self.scan_all(sites)
            await asyncio.sleep(interval)


