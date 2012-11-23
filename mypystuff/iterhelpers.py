import collections
def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

def equalsplits(l, k, iterate = True):
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
