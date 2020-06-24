import unittest.mock as mock
import pytest

from aiohttp.client import ClientResponseError

from pytest import fixture

from sitemon.kafka import SiteReport
from .scanner import Scanner
from .config import Config, SiteConfig

class _TestClient:
    def __init__(self, sites):
        self.sites = sites

    async def get(self, url):
        result = self.sites[url]
        if isinstance(result, Exception):
            raise result

        return 200, result


client = _TestClient({
    'url1': 'result1',
    'error': Exception('err_text'),
    'error_code': ClientResponseError(None, None, code=400, message='client_error'),
})


@pytest.mark.asyncio
async def test_simple():
    '''Scan single site
    '''
    producer = mock.AsyncMock()

    scanner = Scanner(producer, client)
    await scanner.scan_site('url1')
    producer.send_report.assert_called_with(SiteReport(
        url='url1',
        response_code=200,
        response_time=mock.ANY,
    ))


@pytest.mark.asyncio
async def test_regex():
    '''Scan single site with matching pattern
    '''
    producer = mock.AsyncMock()
    scanner = Scanner(producer, client)
    await scanner.scan_site('url1', 'sul')
    producer.send_report.assert_called_with(SiteReport(
        url='url1',
        response_code=200,
        response_time=mock.ANY,
        pattern='sul',
        pattern_match=True,
    ))


@pytest.mark.asyncio
async def test_regex_mismatch():
    '''Scan single site with mismatching pattern
    '''
    producer = mock.AsyncMock()
    scanner = Scanner(producer, client)
    await scanner.scan_site('url1', 'unknown')
    producer.send_report.assert_called_with(SiteReport(
        url='url1',
        response_code=200,
        response_time=mock.ANY,
        pattern='unknown',
        pattern_match=False,
    ))


@pytest.mark.asyncio
async def test_error():
    '''Scan site with error
    '''
    producer = mock.AsyncMock()
    scanner = Scanner(producer, client)
    await scanner.scan_site('error')
    producer.send_report.assert_called_with(SiteReport(
        url='error',
        response_time=mock.ANY,
        error_text='err_text',
    ))


@pytest.mark.asyncio
async def test_scan_multiple():
    '''Scan multiple sites
    '''
    producer = mock.AsyncMock()
    scanner = Scanner(producer, client)
    await scanner.scan_all([
        SiteConfig(url='url1', pattern='su'),
        SiteConfig(url='error'),
    ])

    producer.send_report.assert_any_call(SiteReport(
        url='url1',
        response_code=200,
        response_time=mock.ANY,
        pattern='su',
        pattern_match=True,
    ))
    # producer.send_report.assert_any_call('topic', {
    #     'url': 'error', 'error': 'err_text', 'response_time': mock.ANY,
    # })
