import collections

def isiterable(thing):
    return isinstance(thing, collections.Iterable)

# flatten l, which may be nested to any depth
def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

# split l into k equal sized part
def equalsplits(l, k, iterate=True):
    try:
        q, r = len(l) / k, len(l) % k
        iterable = True
    except TypeError:
        q, r = l / k, l % k
        iterable = False
    indices = [(q * i) + min(i, r) for i in range(k + 1)]
    if iterate and iterable:
        I = iter(l)
        return ([I.next() for i in range(s, e)] for s, e in zip(indices, indices[1:]))
    return indices

# split l into n-grams
def ngrams(l, n=2, pad=False, begin_pad='<s>', end_pad='</s>'):
    if pad:
        pad_size = n / 2
        l = ([begin_pad] * pad_size) + l + ([end_pad] * pad_size)
    return zip(*[l[i:] for i in range(n)])

# split l into chunks of size s, padding optionally
def chunks(l, s, pad=True):
    if pad:
        return map(None, *(iter(l),) * s)
    else:
        return zip(*(iter(l),) * s)

