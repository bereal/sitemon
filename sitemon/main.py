import argparse
import asyncio

from sitemon.scanner import run as run_scanner
from sitemon.status import run as run_status


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('command', choices=('producer', 'consumer'))
    ap.add_argument('-c', '--config', required=True)
    args = ap.parse_args()

    run = {
        'producer': run_scanner,
        'consumer': run_status,
    }[args.command]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(args.config))


if __name__ == '__main__':
    main()

