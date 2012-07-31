def chunkiter(l, s, pad = True):
    if pad:
        return map(None, *(iter(l),) * s)
    else:
        return zip(*(iter(l),) * s)

