import sys

import countrynames
import pycountry


def map_keys(dictionary: dict[str, any], mapping_function) -> dict[str, any]:
    return {mapping_function(k): v for k, v in dictionary.items()}


def country_name_to_english(name: str) -> str:
    try:
        return pycountry.countries.get(alpha_2=countrynames.to_code(name)).name
    except LookupError:
        print('Unexpected country name: "' + name + '"', file=sys.stderr)
        return name
