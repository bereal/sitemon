import dataclasses

import aiopg
from sitemon.kafka import SiteReport

schema = [
    '''
    CREATE TABLE IF NOT EXISTS site_status (
        url            TEXT PRIMARY KEY,
        last_checked   TIMESTAMP NOT NULL DEFAULT NOW(),
        response_time  INT NOT NULL,
        response_code  INT,
        error_text     TEXT,
        pattern        TEXT,
        pattern_match  BOOLEAN
    );
    '''
]


class StatusPersistence:
    def __init__(self, pool: aiopg.Pool):
        self._pool = pool

    @asynccontextmanager
    async def _cursor(self) -> DictCursor:
        async with self.pool.acquire() as conn:
            async with conn.cursor(cursor_factory=DictCursor) as cur:
                await cur.execute('BEGIN')
                try:
                    yield cur
                except:
                    await cur.execute('ROLLBACK')
                    raise
                else:
                    await cur.execute('COMMIT')

    async def init_schema(self):
        async with self._cursor() as cur:
            for s in schema:
                await cur.execute(s);

    async def update_report(self, report: SiteReport):
        async with self._cursor() as cur:
            await cur.execute(
                '''
                INSERT INTO site_status (
                    url, response_time, response_code, error_text, pattern, pattern_match
                ) VALUES (
                    %(url)s, %(response_time)s, %(response_code)s, %(error_text)s, %(pattern)s, %(pattern_match)s
                ) ON CONFLICT DO UPDATE SET
                    url=%(url)s,
                    response_time=%(response_time)s,
                    response_code=%(response_code)s,
                    pattern=%(pattern)s,
                    pattern_match=%(pattern_match)s
                ''', dataclasses.asdict(report)
            )

