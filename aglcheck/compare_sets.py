from . import algorithms as alg

__all__ = ['availableanalysisfunctions', 'crosscorrelationmax',
           'sharedlengthnsubstringcount', 'longestsharedsubstringlength',
           'longestsharedsubstringduration', 'novellengthnsubstringcount',
           'commonstartduration', 'commonstartlength', 'issubstring', 'issame',
           'samestart', 'levenshtein']


class ComparisonMatrix(object):
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


def _analyze_stringbystring(stringdata, analysisf, dataaccessf,
                            title=None, comparison=('All', 'All')):
    """
    Private function that takes string data sets, applies an analysis function
    to each string from the first set in `comparison` with each string from 
    the second set in `comparison`. The sets should be defined in `stringdata`.

    The analysisf must take two strings as the first two arguments and 
    readingframe as the third.

    The dataaccessf can be used to further process the results of the
    analysisf before the result is returned. E.g. count the number of items
    returned by analysisf.

    Parameters
    ----------
    stringdata
    analysisf : a function
        The function compares two strings and returns an outcome. It must take 
        two strings as the first two arguments and readingframe as the third.
    dataaccessf : a function
    title
    comparison

    Returns
    -------
    A ComparisonMatrix instance that can be used for further analyses or 
    visualization.

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
    return ComparisonMatrix(resultsdict=results,
                            dataaccessfunc=dataaccessf,
                            stringdata=stringdata,
                            comparison=comparison,
                            title=title)


def longestsharedsubstringlength(stringdata, comparison=('All', 'All')):
    def analysisf(s1, s2, readingframe):
        items = alg.longestsharedsubstrings(s1, s2, readingframe=readingframe)
        if items:
            return int(len(items[0][0]) / readingframe)
        else:
            return 0

    def dataaccessfunc(count):
        return count

    title = 'Length longest shared substring'
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title=title, comparison=comparison)


def longestsharedsubstringduration(stringdata, comparison=('All', 'All')):
    def analysisf(s1, s2, readingframe):
        return alg.longestsharedsubstringduration(s1, s2,
                                                  tokendurations=stringdata.tokendurations,
                                                  isiduration=stringdata.isiduration,
                                                  readingframe=readingframe)

    def dataaccessfunc(duration):
        return duration

    title = 'Duration longest shared substring'
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title=title, comparison=comparison)


def crosscorrelationmax(stringdata, comparison=('All', 'All')):
    analysisf = alg.crosscorrelate

    def dataaccessfunc(items): return max(items[0])

    title = 'Maximum crosscorrelation'
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title=title, comparison=comparison)


def sharedlengthnsubstringcount(stringdata, n, comparison=('All', 'All')):
    def analysisf(s1, s2, readingframe):
        return alg.sharedlengthnsubstrings(s1, s2, n, readingframe)

    def dataaccessfunc(item):
        if item != ():
            return sum([len(c[1]) for c in item])
        else:
            return 0

    title = 'Number of {}-length shared substrings'.format(n)
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title=title, comparison=comparison)


def novellengthnsubstringcount(stringdata, n, comparison=('All', 'All')):
    def analysisf(s1, s2, readingframe):
        return alg.novellengthnsubstrings(s2, s1, n, readingframe)

    def dataaccessfunc(item):
        if item != ():
            return len(item)
        else:
            return 0

    title = 'Number of novel {}-length substrings'.format(n)
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title=title, comparison=comparison)


def commonstartlength(stringdata, comparison=('All', 'All')):
    analysisf = alg.commonstartlength

    def dataaccessfunc(item): return item

    title = "Length of shared start substring"
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title=title, comparison=comparison)


def commonstartduration(stringdata, comparison=('All', 'All')):
    def analysisf(s1, s2, readingframe):
        return alg.commonstartduration(s1, s2,
                                       tokendurations=stringdata.tokendurations,
                                       isiduration=stringdata.isiduration,
                                       readingframe=readingframe)

    def dataaccessfunc(duration): return duration

    title = 'Duration of shared start substring'
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title=title, comparison=comparison)


def issame(stringdata, comparison=('All', 'All')):
    def analysisf(s1, s2, readingframe): return s1 == s2

    def dataaccessfunc(item): return item

    title = 'Identical strings'
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title=title, comparison=comparison)


def issubstring(stringdata, comparison=('All', 'All')):
    analysisf = alg.issubstring

    def dataaccessfunc(item): return item

    title = 'Is substring'
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title=title, comparison=comparison)


def samestart(stringdata, n, comparison=('All', 'All')):
    def analysisf(s1, s2, readingframe):
        return alg.samestart(s1, s2, n, readingframe)

    def dataaccessfunc(item): return item

    title = 'Has same {}-length substring start'.format(n)
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title, comparison=comparison)


def levenshtein(stringdata, comparison=('All', 'All')):
    def analysisf(s1, s2, readingframe):
        return alg.levenshtein(s1, s2, readingframe)

    def dataaccessfunc(item): return item

    title = 'Levenshtein distance'
    return _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                   title, comparison=comparison)


availableanalysisfunctions = {
    'crosscorrelationmax': crosscorrelationmax,
    'sharedlengthnsubstringcount': sharedlengthnsubstringcount,
    'longestsharedsubstringlength': longestsharedsubstringlength,
    'longestsharedsubstringduration': longestsharedsubstringduration,
    'novellengthnsubstringcount': novellengthnsubstringcount,
    'commonstartduration': commonstartduration,
    'commonstartlength': commonstartlength,
    'issubstring': issubstring,
    'issame': issame,
    'samestart': samestart,
    'levenshtein': levenshtein
}
