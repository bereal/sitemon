import asyncio
import sys

from contextlib import asynccontextmanager

@asynccontextmanager
async def connect(factory, *args, **kwargs):
    '''Create Kafka producer or consumer using factory.
    Make few attempts with intervals.
    '''
    connection = factory(*args, **kwargs)
    for i in range(9, -1, -1):
        try:
            async with connection:
                try:
                    yield connection
                except:
                    pass
        except:
            if not i:
                raise
            print('Waiting for Kafka...', file=sys.stderr)
            await asyncio.sleep(3)


