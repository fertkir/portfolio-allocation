import pycountry


def currencies(currency_codes: list[str]) -> dict[str, dict]:
    result = {}
    for currency_code in currency_codes:
        currency = pycountry.currencies.get(alpha_3=currency_code)
        if currency is None:
            continue
        result[currency_code] = {
            'countries': {
                _to_country(currency.alpha_3): 1
            },
            'industries': {
                'None': 1
            },
            'fee': 0,
            'currencies': {
                currency.alpha_3: 1
            },
            'classes': {
                'Cash': 1
            }
        }
    return result


def _to_country(currency: str) -> str:
    # todo why Europe is missing in the database?
    return 'Europe' if currency == 'EUR' else pycountry.countries.get(alpha_2=currency[0:2]).name
