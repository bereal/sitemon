import argparse
import asyncio

from sitemon.scanner import run as run_scanner

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('command', choices=('producer', 'consumer'))
    ap.add_argument('-c', '--config', required=True)
    args = ap.parse_args()

    if args.command == 'producer':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_scanner(args.config))

if __name__ == '__main__':
    main()

