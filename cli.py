#!/usr/bin/env python

"""
CLI for Eat Bacon.
"""

__author__ = "Przemyslaw I."
__copyright__ = "Copyright 2022, Przemyslaw I."
__license__ = "MIT"
__version__ = "0.1.0"

import argparse
from eat_bacon import EatBacon

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Parses Beacon data')
    parser.add_argument('url', type=str, help='Beacon URL')
    parser.add_argument('--config',
        type=str,
        default='config.json',
        help='Location of the config file'
    )
    args = parser.parse_args()

    # Main run.
    eb = EatBacon(args.url, args.config)
    if eb.get_init_call():
        status = 7 # pylint: disable=invalid-name
        while (status in [1, 3, 7]):
            # Get & parse datapoint
            dp = eb.get_datapoint()
            bacon = EatBacon.parse_datapoint(dp)
            # Make output
            eb.make_output(bacon)
            # Set status
            status = bacon[0]
            # Sleep
            eb.sleep()
