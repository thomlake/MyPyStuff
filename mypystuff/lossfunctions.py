import numpy as np

def precision(cm):
    if isinstance(cm, ConfusionMatrix):
        tp, fp = cm.tp, cm.fp
    else:
        tp, fp = cm[1,1], cm[1,0]
    try:
        return tp / (tp + fp)
    except ZeroDivisionError:
        return 0

def recall(cm):
    if isinstance(cm, ConfusionMatrix):
        tp, fn = cm.tp, cm.fn
    else:
        tp, fn = cm[1,1], cm[0,1]
    try:
        return tp / (tp + fn)
    except ZeroDivisionError:
        return 0

def fmeasure(cm, beta = 1.):
    if isinstance(cm, ConfusionMatrix):
        tp, fp, fn = cm.tp, cm.fp, cm.fn
    else:
        tp, fp, fn = cm[1,1], cm[1,0], cm[0,1]
    try:
        return ((1. + beta**2) * precision * recall) / (beta**2 * precision + recall)
    except ZeroDivisionError:
        return 0

def error(cm):
    if isinstance(cm, ConfusionMatrix):
        mat = cm.mat
    return 1. - (mat.diagonal().sum() / float(mat.sum()))

class ConfusionMatrix(object):
    def __init__(self, n):
        self.n = n
        self.mat = np.zeros((n, n))
    
    @property
    def tn(self):
        return self.mat[0,0]
    
    @property
    def fn(self):
        return self.mat[0,1]
    
    @property
    def fp(self):
        return self.mat[1,0]

    @property
    def tp(self):
        return self.mat[1,1]
    
    def __repr__(self):
        mat = self.mat.astype(int)
        formatstring = '{{0: ^{0}}}'.format(len(str(mat.max())) + 2)
        rows = ['|'.join(formatstring.format(x) for x in row) for row in mat]
        line = '-' * len(rows[0])
        outerline = '      ' + line + '\n'
        innerline = 'pred |' + line + '|\n'
        rows = ['     |' + row + '|\n' for row in rows]
        innerindex = self.n / 2
        header = 'actual'.center(len(outerline)) + '\n'
        rep = header
        for i, row in enumerate(rows):
            if i == innerindex:
                rep += innerline
            else:
                rep += outerline
            rep += row
        rep += outerline
        return rep

    def recall(self):
        return recall(self)
    
    def precision(self):
        return precision(self)
    
    def fmeasure(self, beta = None):
        return fmeasure(self) if beta is None else fmeasure(beta)
    
    def error(self):
        return error(self)

    def update(self, prediction = 0, actual = 0):
        try:
            for p, a in zip(prediction, actual):
                self.mat[prediction, actual] += 1
        except TypeError:
            self.mat[prediction, actual] += 1

TAU = 1e-10
def log_loss(t, o):
    return -t * np.log(o + TAU) - (1 - t) * np.log(1 - o + TAU)

def multiclass_log_loss(t, o):
    return -np.log(o[t.argmax()] + TAU)

def square_loss(t, o):
    return (t - o)**2

