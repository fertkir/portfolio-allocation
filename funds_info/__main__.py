import argparse
import json

if __name__ == '__main__':
    from __init__ import get

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('instruments', metavar='instrument', type=str, nargs='+',
                            help='an instrument to get info for')
    args = vars(arg_parser.parse_args())

    print(json.dumps(get(args['instruments']), indent=2, ensure_ascii=False))
