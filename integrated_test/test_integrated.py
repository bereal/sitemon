import asyncio
import re

import aiopg
import pytest

from datetime import datetime
from psycopg2.extras import DictCursor


@pytest.fixture
async def pool():
    async with aiopg.create_pool(
            host='localhost',
            port=6543,
            user='postgres',
            password='password',
            dbname='postgres') as pool:
        yield pool


@pytest.fixture
async def cursor(pool):
    with await pool.cursor(cursor_factory=DictCursor) as cur:
        yield cur


async def get_snapshot(cursor):
    '''Get all the site info as { url: info }
    '''
    records = {}
    await cursor.execute('SELECT * FROM site_status')
    for row in await cursor.fetchall():
        records[row['url']] = dict(row)

    return records


expected_data = {
    'http://httpbin/anything?match': {
        'pattern_match': True,
        'response_code': 200,
    },
    'http://httpbin/anything?wontmatch': {
        'pattern_match': False,
        'response_code': 200,
    },
    'http://httpbin/status/500': {
        'response_code': 500,
    },
    'http://idontexist/': {
        'response_code': None,
        'error_text': re.compile('Cannot connect'),
    },
}

@pytest.mark.integrated
@pytest.mark.asyncio
async def test_flow(cursor):
    '''Test that the flow works end to end
    '''
    before = await get_snapshot(cursor)
    before_ts = datetime.utcnow()

    await asyncio.sleep(7)
    after = await get_snapshot(cursor)

    assert after != before

    # make sure that the known sites are updated and data is valid
    for url, data in expected_data.items():
        site_data = after[url]
        assert site_data['last_checked'] > before_ts
        for k, v in data.items():
            if isinstance(v, re.Pattern):
                assert v.match(site_data[k])
            else:
                assert site_data[k] == v
