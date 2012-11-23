def getngrams(D, n = 2):
    return zip(*[D[i:] for i in range(n)])

