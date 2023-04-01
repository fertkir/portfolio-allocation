import json
import os

_SECURITIES_CUSTOM_JSON = os.path.join(
    os.environ.get('APPDATA') or
    os.environ.get('XDG_CONFIG_HOME') or
    os.path.join(os.environ['HOME'], '.config'),
    "portfolio-allocation",
    "securities-custom.json"
)


def custom(tickers: list[str]) -> dict[str, dict]:
    if not os.path.exists(_SECURITIES_CUSTOM_JSON):
        print("No custom config \"" + _SECURITIES_CUSTOM_JSON + "\", ignoring it")
        return {}
    print("Reading custom config \"" + _SECURITIES_CUSTOM_JSON + "\"")
    f = open(_SECURITIES_CUSTOM_JSON, "r")
    configs = json.loads(f.read())
    result = {}
    for config in configs:
        instrument = config['instrument']
        if instrument in tickers:
            config.pop('instrument', None)
            result[instrument] = config
    return result
