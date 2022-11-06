from funds_info import currencies, funds


def get_instruments_info(instruments: list[str]) -> dict[str, dict]:
    info_by_currency = currencies.currencies(instruments)
    _currencies = info_by_currency.keys()
    not_currencies = list(filter(lambda instr: instr not in _currencies, instruments))
    info_by_fund = funds.funds(not_currencies)
    _funds = info_by_fund.keys()
    other = list(filter(lambda instr: instr not in _funds, not_currencies))
    return info_by_currency | info_by_fund
