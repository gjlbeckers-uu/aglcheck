import numpy as np
from .stringcomparison import longestsharedsubstrings, crosscorrelate, startswith, \
                        issubstring, commonstart
from .stringsetcomparison import _analyze_stringbystring

__all__ = ['availableanalysisfunctions', 'crosscorrelationmaxtable',
           'htmltable', 'issubstringtable', 'longestsharedsubstringstable',
           'save_html', 'startswithtable']


def htmlcolor_string(s, color='#FF4500'):
    return '<span style="color:{}">{}</span>'.format(color, s)


def htmlcolor_substrings(ss, s, position=None, color='#FF4500'):
    if position is None:
        return s.replace(ss,
                         '<span style="color:{}">{}</span>'.format(color, ss))
    else:
        p1 = s[:position]
        p2 = ss
        remainder = position + len(ss)
        if remainder < len(s):
            p3 = s[remainder:]
        else:
            p3 = ''
        return '{}<span style="color:{}">{}</span>{}'.format(p1, color, p2, p3)

def save_html(htmlcode, filename, include_doctags=True):
    with open(filename, 'w', encoding='utf-8') as f:
        if include_doctags:
            header = '<!DOCTYPE html>' \
                     '<html>' \
                     '<head>' \
                     '<meta charset="UTF-8">' \
                     '<title></title>' \
                     '</head>' \
                     '<body>'
            f.write(header)
        f.write(htmlcode)
        if include_doctags:
            footer = '</body>'
            f.write(footer)


def htmltable(comparisontable, title=None, transpose=False):

        ct = comparisontable
        if title is None:
            title = ct.title
        matrix = ct.get_matrix()
        xstringlabels = ct.xstringlabels
        ystringlabels = ct.ystringlabels
        if not transpose:
            matrix = [list(i) for i in zip(*matrix)]  # we have to transpose
        else:
            xstringlabels, ystringlabels = ystringlabels, xstringlabels
        htmltext = '<style>thead {align:center;}' \
                   'tbody {color:black;}' \
                   'table, th, td {border: 1px solid black; border-collapse: '\
                   'collapse;} th, td {padding: 15px;}' \
                   '</style>'
        htmltext += '<table>'
        htmltext += '<caption>{}</caption>'.format(title)
        htmltext += '<thead><tr><th></th>'
        t = ['<th scope="col"><span style="color:{}">{}</span>'
             '<br>{}</th>'.format(ct.stringdata.stringlabelcolors[xs], xs,
                                  ct.stringdata.stringdict[xs])
            for xs in xstringlabels]
        htmltext += ''.join(t)
        htmltext += '</tr></thead>'
        for rown, row in enumerate(matrix):
            htmltext += '<tr>'
            sl = ystringlabels[rown]
            htmltext += '<th scope="row"><span style="color:{}">{}</span>' \
                        '<br>{}</th>'.format(ct.stringdata.stringlabelcolors[sl], sl,
                                             ct.stringdata.stringdict[sl])
            for coln, cell in enumerate(row):
                htmltext += '<td>'
                for entry in cell:
                    htmltext += '{}<br>'.format(entry)
                htmltext += '</td>'
            htmltext += '</tr>'
        htmltext += '</table>'
        return htmltext

# FIXME refactor this
def longestsharedsubstringstable(stringdata, minlen=1, comparison=('All', 'All'),
                                 title='Longest shared substrings',
                                 transpose=False):

    hc = htmlcolor_substrings

    def analysisf(s1, s2, readingframe):
        if transpose:
            return ['{}&nbsp;&nbsp;{}'.format(hc(ss, s1, position=pos[0]*readingframe),
                                              hc(ss, s2, position=pos[1]*readingframe))
                    for (ss, positions) in
                    longestsharedsubstrings(s1, s2, readingframe)
                    for pos in positions if len(ss) >= minlen]
        else:
            return ['{}&nbsp;&nbsp;{}'.format(hc(ss, s2, position=pos[1]*readingframe),
                                              hc(ss, s1, position=pos[0]*readingframe))
                    for (ss, positions) in longestsharedsubstrings(s1, s2, readingframe)
                    for pos in positions if len(ss) >= minlen]

    def dataaccessfunc(items):
        return items

    cm = _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                 title=title, comparison=comparison)
    return htmltable(cm, transpose=transpose)


def commonstartsubstringstable(stringdata, comparison=('All', 'All'),
                           title='Shared start substring matches', transpose=False):

    hc = htmlcolor_substrings

    def analysisf(s1, s2, readingframe):
        ss = commonstart(s1, s2, readingframe)
        if ss:
            if transpose:
                return ['{}&nbsp;&nbsp;{}'.format(hc(ss, s1, position=0),
                                                  hc(ss, s2, position=0))]
            else:
                return ['{}&nbsp;&nbsp;{}'.format(hc(ss, s2, position=0),
                                                  hc(ss, s1, position=0))]
        else:
            return ''

    def dataaccessfunc(items):
        return items

    cm = _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                 title=title, comparison=comparison)
    return htmltable(cm, transpose=transpose)



def crosscorrelationmaxtable(stringdata, minlen=1, mismatchchar='_',
                             comparison=('All', 'All'),
                             title='Maximum crosscorrelation substring',
                             transpose=False):
    hcs = htmlcolor_string

    def analysisf(s1, s2, readingframe):
        f, s = crosscorrelate(s1, s2, readingframe)
        matches = [np.array(m) for m in np.array(s)[f == np.max(f)]]
        css = []
        for letters in matches:
            if sum(letters != '') >= minlen:
                letters[letters == ''] = mismatchchar * readingframe
                css.append(hcs(''.join(letters).strip(mismatchchar)))
        return css

    def dataaccessfunc(items): return items

    cm = _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                 title=title, comparison=comparison)
    return htmltable(cm, transpose=transpose)

def startswithtable(stringdata, comparison=('All', 'All'),
                    title=None,
                    transpose=False):

    hc = htmlcolor_substrings

    def analysisf(s1, s2, readingframe):
        if startswith(s1, s2, readingframe):
            if transpose:
                return ['{}&nbsp;&nbsp;{}'.format(hc(s2, s1, position=0),
                                                  hc(s2, s2, position=0))]
            else:
                return ['{}&nbsp;&nbsp;{}'.format(hc(s2, s2, position=0),
                                                  hc(s2, s1, position=0))]
        else:
            return ''


    def dataaccessfunc(items): return items

    if title is None:
        if transpose:
            title = 'Row strings starting with complete col string'
        else:
            title = 'Col strings starting with complete row string'

    cm = _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                 title=title, comparison=comparison)
    return htmltable(cm, transpose=transpose)



def issubstringtable(stringdata, comparison=('All', 'All'), title=None,
                     transpose=False):

    hc = htmlcolor_substrings

    def analysisf(s1, s2, readingframe):
        if issubstring(s1, s2, readingframe):
            if transpose:
                return ['{}&nbsp;&nbsp;{}'.format(hc(s1, s1),hc(s1, s2))]
            else:
                return ['{}&nbsp;&nbsp;{}'.format(hc(s1, s2), hc(s1, s1))]
        else:
            return ''

    def dataaccessfunc(item): return item

    if title is None:
        if transpose:
            title = 'Row string is substring of col string'
        else:
            title = 'Col string is substring of row string'

    cm = _analyze_stringbystring(stringdata, analysisf, dataaccessfunc,
                                 title=title, comparison=comparison)
    return htmltable(cm, transpose=transpose)


availableanalysisfunctions = {
    'crosscorrelationmaxtable': crosscorrelationmaxtable,
    'issubstringtable': issubstringtable,
    'longestsharedsubstringstable': longestsharedsubstringstable,
    'startswithtable': startswithtable
}