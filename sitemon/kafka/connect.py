import asyncio
import sys

async def connect(f, *args, **kwargs):
    for i in range(9, -1, -1):
        try:
            return f(*args, **kwargs)
        except:
            if not i:
                raise
            print('Waiting for Kafka...', file=sys.stderr)
            await asyncio.sleep(3)

