import numpy as np
from numpy.random import randint as rint
from primes import primes

class uhashint(object):
    def __init__(self, u, m , p = None):
        if p is None:
            p = primes[np.searchsorted(primes, max(u, m))]
        self.p, self.u, self.m = p, u, m
        self.a, self.b = rint(1, p, 2)

    def __call__(self, x):
        return ((self.a * x + self.b) % self.p) % self.m

class uhashstr_variable(object):
    def __init__(self, u, m, p = None):
        if p is None:
            p = primes[np.searchsorted(primes, max(u, m))]
        self.p, self.u, self.m = p, u, m
        self.a = rint(1, p)
        self.h = uhashint(p, m)
        self.c = self.a**np.arange(100).astype(object)
        
    def __call__(self, s):
        l = len(s)
        x = np.fromstring(s, dtype = 'uint8')
        c = self.c[:l]
        #c = self.a**np.arange(l).astype(object)
        #print c
        #raw_input()
        t = (x * c).sum() % self.p.astype(object)
        return self.h(t)

def zeropad(x, k):
    y = np.zeros(k)
    y[:len(x)] = x[:k]
    return y

class uhashstr(object):
    def __init__(self, u, m, p = None, k = 40):
        if p is None:
            p = primes[np.searchsorted(primes, max(u, m))]
        self.p, self.u, self.m, self.k = p, u, m, k
        self.a = rint(1, p, k)
        self.b = rint(1, p, k)
        
    def __call__(self, s):
        x = zeropad(np.fromstring(s, dtype = 'uint8'), self.k)
        return ((self.a * x + self.b) % self.p).sum() % self.m

# below is the same as above, 
# just slightly more complicated
# yielding little speed savings
# SIMPLE > COMPLEX
class uhashstr_wo(object):
    def __init__(self, u, m, p = None, k = 40):
        if p is None:
            p = primes[np.searchsorted(primes, max(u, m))]
        self.p, self.u, self.m, self.k = p, u, m, k
        self.a = rint(1, p, k)
        self.b = rint(1, p, k)
        
    def __call__(self, s):
        x = np.fromstring(s, dtype = 'uint8')
        return (((self.a[:len(x)] * x + self.b[:len(x)]) % self.p).sum() + self.b[len(x):].sum()) % self.m


        
#        a, b, x, m, l = self.a, self.b, self.x, self.m, len(s)
#        x[:l] = np.fromstring(s, dtype = 'uint8')
#        #h = ((a * x) % p).sum() % m
#        h = (((a * x + b)).sum() % p) % m
#        return h

def test_universal_int(u, m, n, l = None):
    print 'u:', u
    print 'm:', m
    print 'n:', n
    X = rint(0, u, n)
    if l:
        H = [uhashint(u, m) for i in range(l)]
        Y = []
        for h in H:
            Y.extend([h(x) for x in X])
    else:
        h = uhashint(u, m)
        Y = [h(x) for x in X]
    import matplotlib.pyplot as plt
    plt.hist(Y, m)
    plt.xlim((0, m))
    plt.show()

def test_universal_str(m, n):
    u = 256
    randstr = lambda: ''.join(map(chr, rint(0, u, rint(3, 25))))
    S = [randstr() for i in range(n)]
    h = uhashstr(u, m)

    H = [h(s) for s in S]

    import matplotlib.pyplot as plt
    #plt.hist(H)
    plt.hist(H, m)
    plt.xlim((0, m))
    plt.show()

if __name__ == '__main__':
    import sys
    flag = sys.argv[1]
    if flag == '-i':
        print '.... testing uhashint'
        test_universal_int(*map(int, sys.argv[2:]))
    if flag == '-s':
        print '.... testing uhashstr'
        test_universal_str(*map(int, sys.argv[2:]))
    else:
        print '.... unknown flag: {0}'.format(flag)
