#!/usr/bin/env python
"""Check if timestamp patterns of packet caught from tcpdump."""

import argparse
import sys

from datetime import datetime, timedelta


TIME_FMT = '%H:%M:%S.%f'


def check_tcpdump_by_time(dumped, max_delta):
    """Iterate thru file and compares time delta between sequential."""
    with open(dumped) as tcpdump:
        previous_time, previous_delta = None, None
        for line in tcpdump:
            current_time = line.split(' ')[0]
            if not previous_time:
                previous_time = current_time
                continue
            current_delta = datetime.strptime(current_time, TIME_FMT) \
                - datetime.strptime(previous_time, TIME_FMT)
            if not previous_delta:
                previous_delta = current_delta
                continue
            if timedelta(milliseconds=-max_delta) \
                    < (current_delta - previous_delta) \
                    > timedelta(milliseconds=max_delta):
                return False
            previous_delta, previous_time = current_delta, current_time
        return True


def cli_args():
    """Parse CLI args."""
    parser = argparse.ArgumentParser(prog='TCP time check')
    parser.add_argument(
        '-f',
        '--file-location',
        action='store',
        dest='location',
        required=True,
        help='Full file path to tcpdumped file'
    )
    parser.add_argument(
        '-m',
        '--max-delta',
        action='store',
        dest='max_delta',
        default=0.5,
        help='Max difference between each delta of '
        'incoming packets in milliseconds.'
    )
    return parser.parse_args()


if __name__ == '__main__':
    ARGS = cli_args()
    if not check_tcpdump_by_time(ARGS.location, ARGS.max_delta):
        sys.exit(1)