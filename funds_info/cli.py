import argparse
import json

import funds_info


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('instruments', metavar='instrument', type=str, nargs='+',
                            help='an instrument to get info for')
    args = vars(arg_parser.parse_args())
    print(json.dumps(funds_info.get_instruments_info(args['instruments']), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
