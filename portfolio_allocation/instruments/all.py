from . import currencies, custom, funds, securities


def get_data(tickers: list[str]) -> dict[str, dict]:
    custom_info = custom.custom(tickers)
    _custom = custom_info.keys()
    not_custom = list(filter(lambda ticker: ticker not in _custom, tickers))
    info_by_currency = currencies.currencies(not_custom)
    _currencies = info_by_currency.keys()
    not_currencies = list(filter(lambda ticker: ticker not in _currencies, not_custom))
    info_by_fund = funds.funds(not_currencies)
    _funds = info_by_fund.keys()
    other = list(filter(lambda ticker: ticker not in _funds, not_currencies))
    _securities = securities.securities(other)
    return custom_info | info_by_currency | info_by_fund | _securities
