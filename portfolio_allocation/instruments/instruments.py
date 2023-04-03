from .sources import currencies, funds, securities


def get_data(tickers: list[str]) -> dict[str, dict]:
    # custom_info = custom.custom(tickers)
    # _custom = custom_info.keys()
    # todo should not filter out if no parameters are set in custom config:
    # not_custom = list(filter(lambda ticker: ticker not in _custom, tickers))
    info_by_currency = currencies.currencies(tickers)
    _currencies = info_by_currency.keys()
    not_currencies = list(filter(lambda ticker: ticker not in _currencies, tickers))
    info_by_fund = funds.funds(not_currencies)
    _funds = info_by_fund.keys()
    other = list(filter(lambda ticker: ticker not in _funds, not_currencies))
    _securities = securities.securities(other)
    result = info_by_currency | info_by_fund | _securities
    # for key, value in result.items():
    #     for
    return result
