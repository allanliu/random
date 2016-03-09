#!/usr/bin/env python
"""Script that can generate tons of orphaned processes."""

import os
import md5
import argparse
import time
from multiprocessing import Process


def kill_cpu(child=False):
    """Kill cpu with md5 sums.

    Spawns a child process on first with option
    """
    if child:
        Process(
            target=kill_cpu,
        ).start()
    while True:
        md5er = md5.new()
        md5er.update("Lorem ipsum dolor sit amet")
        md5er.digest()


def eat_resource(child=False):
    """Create memory consuming child processes.

    Spawns a child process on first with option
    """
    if child:
        Process(
            target=eat_resource,
        ).start()
    while True:
        try:
            ' ' * 51200000
            time.sleep(0.5)
        except OSError:
            continue


def run(orphans, seconds, balance):
    """Spin up a new process and kills itself to orphan children."""
    if balance:
        target = eat_resource
    else:
        target = kill_cpu
    processes = []
    for _ in range(orphans):
        processes.append(
            Process(
                target=target,
                args=(True,),
            )
        )
    for process in processes:
        process.start()
    time.sleep(seconds)
    for process in processes:
        process.terminate()


def cli_args():
    """Parse CLI args."""
    parser = argparse.ArgumentParser(prog='orphaned')
    parser.add_argument(
        '-s',
        '--seconds',
        action='store',
        dest='seconds',
        type=int,
        default=30,
    )
    parser.add_argument(
        '-o',
        '--orphans',
        action='store',
        dest='orphans',
        type=int,
        default=1,
    )
    parser.add_argument(
        '--balance',
        action='store_true',
        dest='balance',
        default=False,
    )
    return parser.parse_args()


if __name__ == '__main__':
    ARGS = cli_args()
    run(ARGS.orphans, ARGS.seconds, ARGS.balance)
