from os.path import expanduser, join, dirname, realpath

from diskcache import Cache

_CACHE_DIR = expanduser(join(dirname(realpath(__file__)), 'cache'))

cache = Cache(_CACHE_DIR)

CACHE_EXPIRATION = 60 * 60 * 24 * 30 # 30 days
