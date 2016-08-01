import numpy as np
from . import algorithms as alg

__all__ = ['crosscorrelationmax', 'lengthnsubstringcount',
           'longestsubstringlength', 'longestsubstringduration',
           'commonstartduration', 'commonstartlength', 'issubstring', 'issame',
           'samestart', 'levenshtein', 'plot_comparison']


class ComparisonTable(object):
    def __init__(self, resultsdict, dataaccessfunc,
                 stringdata, stringgroups, title=None):

        self.resultsdict = resultsdict
        self.dataaccessfunc = dataaccessfunc
        self.stringdata = stringdata
        self.stringgroups = stringgroups
        self.labelcolors = stringdata.labelcolors
        if not stringdata.subgroups == {}:
            self.subgroups = stringdata.subgroups
        else:
            self.subgroups = stringgroups
        self.colorlabels = dict(
            (s, c) for c, sl in self.labelcolors.items() for s in sl)
        for label, string in stringdata.stringdict.items():
            if label not in self.colorlabels:
                self.colorlabels[label] = 'black'
        self.title = title

    def get_matrix(self):
        xstringlabels = list(self.stringgroups[1].values())[0]
        ystringlabels = list(self.stringgroups[0].values())[0]
        matrix = []
        for yl in ystringlabels:
            cols = []
            for xl in xstringlabels:
                result = self.dataaccessfunc(self.resultsdict[yl][xl])
                cols.append(result)
            matrix.append(cols)
        return matrix

    def get_pandaseries(self):
        import pandas as pd
        indextuples = []
        values = []
        for l1 in list(self.stringgroups[0].values())[0]:
            g1 = None
            for key, labels in self.subgroups.items():
                if l1 in labels:
                    g1 = key
            for l2 in self.stringgroups[1].values()[0]:
                g2 = None
                for key, labels in self.subgroups.items():
                    if l2 in labels:
                        g2 = key
                indextuples.append((g1, g2, l1, l2))
                values.append(self.dataaccessfunc(self.resultsdict[l1][l2]))
        names = ['subgroups_{}'.format(sg.keys()[0])
                 for sg in self.stringgroups]
        names.extend(['strings_{}'.format(sg.keys()[0])
                      for sg in self.stringgroups])
        index = pd.MultiIndex.from_tuples(indextuples, names=names)
        return pd.Series(values, index=index)


def _analyze_dataset(stringdata, analysisf, dataaccessf,
                     title=None, comparison='full'):
    stringgroups = stringdata.comparisons[comparison]
    rf = stringdata.readingframe
    results = {}
    for s1label in list(stringgroups[0].values())[0]:
        results[s1label] = {}
        for s2label in list(stringgroups[1].values())[0]:
            s1 = stringdata.stringdict[s1label]
            s2 = stringdata.stringdict[s2label]
            results[s1label][s2label] = analysisf(s1, s2, readingframe=rf)
    return ComparisonTable(resultsdict=results,
                           dataaccessfunc=dataaccessf,
                           stringdata=stringdata,
                           stringgroups=stringgroups,
                           title=title)


def longestsubstringlength(stringdata, comparison='full'):

    def analysisf(s1, s2, readingframe):
        items = alg.longestsubstrings(s1, s2, readingframe=readingframe)
        if items:
            return int(len(items[0][0]) / readingframe)
        else:
            return 0

    def dataaccessfunc(count):
        return count

    title = 'Length longest substring match'
    return _analyze_dataset(stringdata, analysisf, dataaccessfunc,
                            title=title, comparison=comparison)


def longestsubstringduration(stringdata, comparison='full'):
    def analysisf(s1, s2, readingframe):
        return alg.longestsubstringduration(s1, s2,
                                            tokendurations=stringdata.tokendurations,
                                            isiduration=stringdata.isiduration,
                                            readingframe=readingframe)

    def dataaccessfunc(duration):
        return duration
    title = 'Duration longest substring match'
    return _analyze_dataset(stringdata, analysisf, dataaccessfunc,
                            title=title, comparison=comparison)

def crosscorrelationmax(stringdata, comparison='full'):

    analysisf = alg.crosscorrelate

    def dataaccessfunc(items): return max(items[0])

    title = 'Maximum crosscorrelation'
    return _analyze_dataset(stringdata, analysisf, dataaccessfunc,
                            title=title, comparison=comparison)


def lengthnsubstringcount(stringdata, n, comparison='full'):

    def analysisf(s1, s2, readingframe):
        return alg.lengthnsubstrings(s1, s2, n, readingframe)

    def dataaccessfunc(item):
        if item != ():
            return sum([len(c[1]) for c in item])
        else:
            return 0
    title = 'Number of {}-length substring matches'.format(n)
    return _analyze_dataset(stringdata, analysisf, dataaccessfunc,
                            title=title, comparison=comparison)


def commonstartlength(stringdata, comparison='full'):
    analysisf = alg.commonstartlength

    def dataaccessfunc(item): return item

    title = "Length of shared start substring"
    return _analyze_dataset(stringdata, analysisf, dataaccessfunc,
                            title=title, comparison=comparison)


def commonstartduration(stringdata, comparison='full'):
    def analysisf(s1, s2, readingframe):
        return alg.commonstartduration(s1, s2,
                                       tokendurations=stringdata.tokendurations,
                                       isiduration=stringdata.isiduration,
                                       readingframe=readingframe)

    def dataaccessfunc(duration): return duration
    title = 'Duration of shared start substring'
    return _analyze_dataset(stringdata, analysisf, dataaccessfunc,
                            title=title, comparison=comparison)


def issame(stringdata, comparison='full'):

    def analysisf(s1, s2, readingframe): return s1 == s2

    def dataaccessfunc(item): return item

    title = 'Identical strings'
    return _analyze_dataset(stringdata, analysisf, dataaccessfunc,
                            title=title, comparison=comparison)


def issubstring(stringdata, comparison='full'):

    analysisf = alg.issubstring

    def dataaccessfunc(item): return item

    title = 'Is substring'
    return _analyze_dataset(stringdata, analysisf, dataaccessfunc,
                            title=title, comparison=comparison)

def samestart(stringdata, n, comparison='full'):

    def analysisf(s1, s2, readingframe):
        return alg.samestart(s1, s2, n, readingframe)

    def dataaccessfunc(item): return item

    title = 'Has same {}-length substring start'.format(n)
    return _analyze_dataset(stringdata, analysisf, dataaccessfunc,
                            title, comparison=comparison)


def levenshtein(stringdata, comparison='full'):

    def analysisf(s1, s2, readingframe):
        return alg.levenshtein(s1, s2, readingframe)

    def dataaccessfunc(item): return item

    title = 'Levenshtein distance'
    return _analyze_dataset(stringdata, analysisf, dataaccessfunc,
                            title, comparison=comparison)

def plot_comparison(comparisontable, cmap=None,
                    colorbarorientation='vertical',
                    colorbarshrink=1., clim=None, colorbarlabel='',
                    title=None):

    import matplotlib.pyplot as plt

    ct = comparisontable
    if title is None:
        title = ct.title
        if title is None:
            title = ''
    matrix = ct.get_matrix()
    matrix = np.array(matrix)
    mmin, mmax = matrix.min(), matrix.max()
    if np.issubdtype(matrix.dtype, np.int):
        intcolors = True
    else:
        intcolors = False
    if intcolors:
        if clim is None:
            clim = (mmin - 0.5, mmax + 0.5)
            ticks = [t for t in range(mmin, mmax + 1)]
            lut = mmax - mmin + 1
        else:
            ticks = [t for t in range(clim[0], clim[1] + 1)]
            lut = clim[1] - clim[0] + 1
    else:
        ticks = None
        lut = None
    if cmap is None:
        if intcolors:
            cmap = plt.cm.get_cmap('jet', lut)
        else:
            cmap = plt.cm.get_cmap('viridis', lut)
    else:
        cmap = plt.cm.get_cmap(cmap, lut)
    xstringlabels = list(ct.stringgroups[1].values())[0]
    ystringlabels = list(ct.stringgroups[0].values())[0]
    ax = plt.gca()
    plt.imshow(matrix, interpolation='nearest', cmap=cmap, clim=clim)
    plt.xticks(np.arange(len(xstringlabels)), xstringlabels)
    plt.yticks(np.arange(len(ystringlabels)), ystringlabels)
    plt.xticks(rotation=70)
    for color, category in ct.labelcolors.items():
        for xticklabel in ax.get_xticklabels():
            if xticklabel.get_text() in category:
                xticklabel.set_color(color)
        for yticklabel in ax.get_yticklabels():
            if yticklabel.get_text() in category:
                yticklabel.set_color(color)
    plt.title(title)
    plt.colorbar(orientation=colorbarorientation,
                 ticks=ticks,
                 shrink=colorbarshrink,
                 label=colorbarlabel)
