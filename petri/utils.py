import math
import random
import string
import itertools
import sys

from zlib import adler32

import mulli

trans_table = str.maketrans(dict((k, None) for k in string.punctuation))


def create_short_id(url):
    url = url.translate(trans_table).lower()

    try:
        max_int = int(url, base=36)
    except ValueError:
        raise
    else:
        if max_int >= sys.float_info.max:
            max_int = adler32(mulli.int_to_bytes(max_int))
        max_int = round(math.sqrt(math.sqrt(max_int)))

    urls = mulli.load_database()
    for _ in itertools.repeat(None, max_int):
        short_id = random.randint(1, max_int)
        if short_id not in urls:
            return short_id
    raise ValueError


def save_url(id, url, valid=365):
    entry = {'url': url}
    mulli.add_entry(id, entry, valid)


def load_url(id):
    url = mulli.load_entry(id)
    return url['url']
