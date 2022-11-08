from portfolio_allocation.instruments import currencies, funds, securities


def get_data(tickers: list[str]) -> dict[str, dict]:
    info_by_currency = currencies.currencies(tickers)
    _currencies = info_by_currency.keys()
    not_currencies = list(filter(lambda ticker: ticker not in _currencies, tickers))
    info_by_fund = funds.funds(not_currencies)
    _funds = info_by_fund.keys()
    other = list(filter(lambda ticker: ticker not in _funds, not_currencies))
    _securities = securities.securities(other)
    return info_by_currency | info_by_fund | _securities