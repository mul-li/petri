import math
import random
import string
import itertools

import functools

import mulli

load_urls = functools.partial(mulli.load_database, filename='petri.pickle')
save_urls = functools.partial(mulli.save_database, filename='petri.pickle')

trans_table = str.maketrans(dict((k, None) for k in string.punctuation))


def create_short_id(url):
    url = url.translate(trans_table).lower()

    try:
        max_int = int(url, base=36)
    except ValueError:
        raise
    else:
        max_int = round(math.sqrt(math.sqrt(max_int)))

    urls = load_urls()
    for _ in itertools.repeat(None, max_int):
        short_id = random.randint(1, max_int)
        if short_id not in urls:
            return short_id
    raise ValueError


def save_url(id, url, valid=365):
    urls = load_urls()
    entry = {'url': url}
    save_urls(mulli.add_entry(id, entry, valid, urls))


def remove_url(id):
    urls = load_urls()
    del urls[id]
    save_urls(urls)


def load_url(id):
    url = mulli.load_entry(id, load_urls())
    return url['url']
