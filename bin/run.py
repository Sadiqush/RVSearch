import argparse
import sys

import rvsearch.config as vconf
from rvsearch.main import run


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='+', help='The csv file to read')
    parser.add_argument('-o', '--output', help='The path to save the results')
    parser.add_argument('-q', '--quiet', nargs='?', default='talkcyka', help='Be verbose')
    parser.add_argument('-v', '--verbose', nargs='?', default='shutupcyka', help='Be so verbose')

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    if args.quiet is None:
        vconf.QUIET = True
    elif args.quiet == 'talkcyka':
        vconf.QUIET = False
    else:
        raise Exception('Don\'t pass anything to -q argument')
    if args.verbose is None:
        vconf.VERBOSE = True
    elif args.verbose == 'shutupcyka':
        vconf.VERBOSE = False
    else:
        raise Exception('Don\'t pass anything to -v argument')

    sys.exit(run(input_path, output_path))
