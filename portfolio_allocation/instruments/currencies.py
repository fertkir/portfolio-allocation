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
            'industries': {},
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
    return 'Europe' if currency == 'EUR' else pycountry.countries.get(alpha_2=currency[0:2]).name
