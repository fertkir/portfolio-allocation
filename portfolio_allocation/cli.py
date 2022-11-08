import argparse
import json

from portfolio_allocation import instruments, gnucash, report


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Commands description', required=True)

    asset_data = subparsers.add_parser('data', help='Shows currency, fee, allocation data for provided list of tickers')
    asset_data.set_defaults(cmd='data')
    asset_data.add_argument('tickers', metavar='ticker', type=str, nargs='+',
                            help='a ticker of an asset to get info for')

    asset_allocation_gnucash = subparsers.add_parser(
        'gnucash-allocation',
        help='Generates allocation report based on GnuCash\'s Security Piechart and allocation data of its components')
    asset_allocation_gnucash.set_defaults(cmd='gnucash-allocation')
    asset_allocation_gnucash.add_argument(
        "-r", "--report-name",
        help="Name of report which contains securities allocation (default: Securities)",
        nargs='?', const=1, type=str,
        default="Securities")
    asset_allocation_gnucash.add_argument("-f", "--datafile", required=True, type=str,
                                          help="GnuCash datafile (.gnucash)")

    args = parser.parse_args()

    if args.cmd == 'data':
        print(json.dumps(instruments.get_data(args.tickers), indent=2, ensure_ascii=False))
    elif args.cmd == 'gnucash-allocation':
        parsed_gnucash_report = gnucash.get_value_by_instrument(report_name=args.report_name, datafile=args.datafile)
        report.generate(parsed_gnucash_report.value_by_instrument, parsed_gnucash_report.currency)


if __name__ == '__main__':
    main()
