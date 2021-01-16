import argparse
from main import run

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='+', help='The csv file to read')
    parser.add_argument('-o', '--output', help='The path to save the results')

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    run(input_path, output_path)
