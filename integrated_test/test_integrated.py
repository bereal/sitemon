import asyncio
import aiopg
import pytest

from datetime import datetime
from psycopg2.extras import DictCursor


@pytest.fixture
async def pool():
    async with aiopg.create_pool('host=localhost port=5433 user=postgres password=password dbname=postgres') as pool:
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


@pytest.mark.integrated
@pytest.mark.asyncio
async def test_flow(cursor):
    before = await get_snapshot(cursor)
    before_ts = datetime.utcnow()

    await asyncio.sleep(7)

    after = await get_snapshot(cursor)
    assert before != after

    # make sure that the known sites are updated and data is valid

    match_site = after['http://httpbin/anything?match']

    assert match_site['pattern_match']
    assert match_site['last_checked'] > before_ts
    assert match_site['response_code'] == 200

    nomatch_site = after['http://httpbin/anything?wontmatch']

    assert not nomatch_site['pattern_match']
    assert nomatch_site['last_checked'] > before_ts
    assert nomatch_site['response_code'] == 200

    err_site = after['http://httpbin/status/500']
    assert err_site['last_checked'] > before_ts
    assert err_site['response_code'] == 500
