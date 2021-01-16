import argparse
from main import run

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='+', help='The csv file to read')

    args = parser.parse_args()

    input_path = args.input
    run(input_path)
