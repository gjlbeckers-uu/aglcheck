import numpy as np
from . import algorithms as alg

__all__ = ['crosscorrelationmax', 'sharedlengthnsubstringcount',
           'longestsharedsubstringlength', 'longestsharedsubstringduration',
           'novellengthnsubstringcount',
           'commonstartduration', 'commonstartlength', 'issubstring', 'issame',
           'samestart', 'levenshtein', 'plot_comparison']


class ComparisonTable(object):
    def __init__(self, resultsdict, dataaccessfunc,
                 stringdata, comparison, title=None):

        self.resultsdict = resultsdict
        self.dataaccessfunc = dataaccessfunc
        self.stringdata = stringdata
        self.comparison = comparison
        self.title = title
        self.xstringlabels = stringdata.stringcategories[comparison[0]]
        self.ystringlabels = stringdata.stringcategories[comparison[1]]

    def get_matrix(self):

        matrix = []
        for xl in self.xstringlabels:
            cols = []
            for yl in self.ystringlabels:
                result = self.dataaccessfunc(self.resultsdict[xl][yl])
                cols.append(result)
            matrix.append(cols)
        return matrix

    # def get_pandaseries(self):
    #     import pandas as pd
    #     indextuples = []
    #     values = []
    #     for l1 in list(self.stringgroups[0].values())[0]:
    #         g1 = None
    #         for key, labels in self.subgroups.items():
    #             if l1 in labels:
    #                 g1 = key
    #         for l2 in self.stringgroups[1].values()[0]:
    #             g2 = None
    #             for key, labels in self.subgroups.items():
    #                 if l2 in labels:
    #                     g2 = key
    #             indextuples.append((g1, g2, l1, l2))
    #             values.append(self.dataaccessfunc(self.resultsdict[l1][l2]))
    #     names = ['subgroups_{}'.format(sg.keys()[0])
    #              for sg in self.stringgroups]
    #     names.extend(['strings_{}'.format(sg.keys()[0])
    #                   for sg in self.stringgroups])
    #     index = pd.MultiIndex.from_tuples(indextuples, names=names)
    #     return pd.Series(values, index=index)


def _analyze_datastringbystring(stringdata, analysisf, dataaccessf,
                                title=None, comparison=('All','All')):
    """
    Private function that takes string data sets, applies an analysis function
    to each string from a set with each string from another set. Which strings
    are compared is determined by the `comparison` parameter. Default is `full`
    which means that every string is compared with every other string.

    The analysisf must take two strings as the first two arguments.

    The dataaccessf can be used to further process the results of the
    analysisf before the result is returned. E.g. count the number of items
    returned.

    Parameters
    ----------
    stringdata
    analysisf
    dataaccessf
    title
    comparison

    Returns
    -------

    """
    stringcategory0 = stringdata.stringcategories[comparison[0]]
    stringcategory1 = stringdata.stringcategories[comparison[1]]
    rf = stringdata.readingframe
    results = {}
    for s0label in stringcategory0:
        results[s0label] = {}
        for s1label in stringcategory1:
            s0 = stringdata.stringdict[s0label]
            s1 = stringdata.stringdict[s1label]
            results[s0label][s1label] = analysisf(s0, s1, readingframe=rf)
    return ComparisonTable(resultsdict=results,
                           dataaccessfunc=dataaccessf,
                           stringdata=stringdata,
                           comparison=comparison,
                           title=title)

# def _analyze_datastringbystringset(stringdata, analysisf, dataaccessf,
#                              title=None, comparison='full',
#                              setname='stringsa'):
#     stringlabels1 = stringdata.comparisons[comparison][0].items()
#     stringlabels2 = stringdata.comparisons[comparison][1].items()
#

#FIXME add _analyze_datastringbyset
#FIXME add what is ploted against what

def longestsharedsubstringlength(stringdata, comparison=('All','All')):

    def analysisf(s1, s2, readingframe):
        items = alg.longestsharedsubstrings(s1, s2, readingframe=readingframe)
        if items:
            return int(len(items[0][0]) / readingframe)
        else:
            return 0

    def dataaccessfunc(count):
        return count

    title = 'Length longest shared substring'
    return _analyze_datastringbystring(stringdata, analysisf, dataaccessfunc,
                                       title=title, comparison=comparison)


def longestsharedsubstringduration(stringdata, comparison=('All','All')):
    def analysisf(s1, s2, readingframe):
        return alg.longestsharedsubstringduration(s1, s2,
                                                  tokendurations=stringdata.tokendurations,
                                                  isiduration=stringdata.isiduration,
                                                  readingframe=readingframe)

    def dataaccessfunc(duration):
        return duration
    title = 'Duration longest shared substring'
    return _analyze_datastringbystring(stringdata, analysisf, dataaccessfunc,
                                       title=title, comparison=comparison)

def crosscorrelationmax(stringdata, comparison=('All','All')):

    analysisf = alg.crosscorrelate

    def dataaccessfunc(items): return max(items[0])

    title = 'Maximum crosscorrelation'
    return _analyze_datastringbystring(stringdata, analysisf, dataaccessfunc,
                                       title=title, comparison=comparison)


def sharedlengthnsubstringcount(stringdata, n, comparison=('All','All')):

    def analysisf(s1, s2, readingframe):
        return alg.sharedlengthnsubstrings(s1, s2, n, readingframe)

    def dataaccessfunc(item):
        if item != ():
            return sum([len(c[1]) for c in item])
        else:
            return 0
    title = 'Number of {}-length shared substrings'.format(n)
    return _analyze_datastringbystring(stringdata, analysisf, dataaccessfunc,
                                       title=title, comparison=comparison)

def novellengthnsubstringcount(stringdata, n, comparison=('All','All')):

    def analysisf(s1, s2, readingframe):
        return alg.novellengthnsubstrings(s2, s1, n, readingframe)

    def dataaccessfunc(item):
        if item != ():
            return len(item)
        else:
            return 0
    title = 'Number of novel {}-length substrings'.format(n)
    return _analyze_datastringbystring(stringdata, analysisf, dataaccessfunc,
                                       title=title, comparison=comparison)

def commonstartlength(stringdata, comparison=('All','All')):
    analysisf = alg.commonstartlength

    def dataaccessfunc(item): return item

    title = "Length of shared start substring"
    return _analyze_datastringbystring(stringdata, analysisf, dataaccessfunc,
                                       title=title, comparison=comparison)


def commonstartduration(stringdata, comparison=('All','All')):
    def analysisf(s1, s2, readingframe):
        return alg.commonstartduration(s1, s2,
                                       tokendurations=stringdata.tokendurations,
                                       isiduration=stringdata.isiduration,
                                       readingframe=readingframe)

    def dataaccessfunc(duration): return duration
    title = 'Duration of shared start substring'
    return _analyze_datastringbystring(stringdata, analysisf, dataaccessfunc,
                                       title=title, comparison=comparison)


def issame(stringdata, comparison=('All','All')):

    def analysisf(s1, s2, readingframe): return s1 == s2

    def dataaccessfunc(item): return item

    title = 'Identical strings'
    return _analyze_datastringbystring(stringdata, analysisf, dataaccessfunc,
                                       title=title, comparison=comparison)


def issubstring(stringdata, comparison=('All','All')):

    analysisf = alg.issubstring

    def dataaccessfunc(item): return item

    title = 'Is substring'
    return _analyze_datastringbystring(stringdata, analysisf, dataaccessfunc,
                                       title=title, comparison=comparison)

def samestart(stringdata, n, comparison=('All','All')):

    def analysisf(s1, s2, readingframe):
        return alg.samestart(s1, s2, n, readingframe)

    def dataaccessfunc(item): return item

    title = 'Has same {}-length substring start'.format(n)
    return _analyze_datastringbystring(stringdata, analysisf, dataaccessfunc,
                                       title, comparison=comparison)


def levenshtein(stringdata, comparison=('All','All')):

    def analysisf(s1, s2, readingframe):
        return alg.levenshtein(s1, s2, readingframe)

    def dataaccessfunc(item): return item

    title = 'Levenshtein distance'
    return _analyze_datastringbystring(stringdata, analysisf, dataaccessfunc,
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
    matrix = np.array(ct.get_matrix()).T
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
            ticks = [t for t in np.linspace(clim[0], clim[1], clim[1]-clim[0]+1)]
            clim = (clim[0] - 0.5, clim[1] + 0.5)
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
    ax = plt.gca()
    plt.imshow(matrix, interpolation='nearest', cmap=cmap, clim=clim)
    plt.xticks(np.arange(len(ct.xstringlabels)), ct.xstringlabels)
    plt.yticks(np.arange(len(ct.ystringlabels)), ct.ystringlabels)
    plt.xticks(rotation=70)
    for xticklabel in ax.get_xticklabels():
        color = ct.stringdata.stringlabelcolors[xticklabel.get_text()]
        xticklabel.set_color(color)
    for yticklabel in ax.get_yticklabels():
        color = ct.stringdata.stringlabelcolors[yticklabel.get_text()]
        yticklabel.set_color(color)
    plt.title(title)
    plt.colorbar(orientation=colorbarorientation,
                 ticks=ticks,
                 shrink=colorbarshrink,
                 label=colorbarlabel)
    return ax

def plot_comparisons(*args, clim=None, colorbarorientation='vertical',
                     colorbarshrink=1.,colorbarlabel=''):

    import matplotlib.pyplot as plt

    low = np.inf
    high = -np.inf
    for ct in args:
        ar = np.array(ct.get_matrix())
        low = min(low, ar.min())
        high = max(high, ar.max())
        clim = (low, high)
    axes = []
    for i,ct in enumerate(args, 1):
        plt.subplot(1,len(args),i)
        axes.append(plot_comparison(ct, cmap=None,
                                    colorbarorientation=colorbarorientation,
                                    colorbarshrink=colorbarshrink, clim=clim,
                                    colorbarlabel=colorbarlabel,
                                    title=None))
    return axes