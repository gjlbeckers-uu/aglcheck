import numpy as np
from .algorithms import longestsubstrings, crosscorrelate, startswith, \
                        issubstring
from .compare_sets import _analyze_dataset

__all__ = ['crosscorrelationmaxtable', 'htmltable', 'longestsubstringstable',
           'write_html', 'startswithtable', 'issubstringtable']


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

def write_html(htmlcode, filename, include_doctags=True):
    with open(filename, 'w') as f:
        if include_doctags:
            header = '<!DOCTYPE html>' \
                     '<html>' \
                     '<head>' \
                     '<meta charset="UTF-8">' \
                     '<title></title>' \
                     '</head>' \
                     '<body>'
            f.write(header.encode('utf8'))
        f.write(htmlcode.encode('utf8'))
        if include_doctags:
            footer = '</body>'.encode('utf8')
            f.write(footer)


def htmltable(comparisontable, title=None):

        ct = comparisontable
        if title is None:
            title = ct.title
        matrix = ct.get_matrix()
        xstringlabels = list(ct.stringgroups[1].values())[0]
        ystringlabels = list(ct.stringgroups[0].values())[0]
        htmltext = '<style>thead {align:center;}' \
                   'tbody {color:black;}' \
                   'table, th, td {border: 1px solid black; border-collapse: '\
                   'collapse;} th, td {padding: 15px;}' \
                   '</style>'
        htmltext += '<table>'
        htmltext += '<caption>{}</caption>'.format(title)
        htmltext += '<thead><tr><th></th>'
        t = ['<th scope="col"><span style="color:{}">{}</span>'
             '<br>{}</th>'.format(ct.colorlabels[xs], xs,
                                  ct.stringdata.stringdict[xs])
            for xs in xstringlabels]
        htmltext += ''.join(t)
        htmltext += '</tr></thead>'
        for rown, row in enumerate(matrix):
            htmltext += '<tr>'
            sl = ystringlabels[rown]
            htmltext += '<th scope="row"><span style="color:{}">{}</span>' \
                        '<br>{}</th>'.format(ct.colorlabels[sl], sl,
                                             ct.stringdata.stringdict[sl])
            for coln, cell in enumerate(row):
                htmltext += '<td>'
                for entry in cell:
                    htmltext += '{}<br>'.format(entry)
                htmltext += '</td>'
            htmltext += '</tr>'
        htmltext += '</table>'
        return htmltext


def longestsubstringstable(stringdata, minlen=1, comparison='full',
                           title='Longest substring matches'):

    hc = htmlcolor_substrings

    def analysisf(s1, s2, readingframe):
        return ['{}&nbsp;&nbsp;{}'.format(hc(ss, s1, position=pos[0]),
                                          hc(ss, s2, position=pos[1]))
                for (ss, positions) in longestsubstrings(s1, s2, readingframe)
                for pos in positions if len(ss) >= minlen * readingframe]

    def dataaccessfunc(items):
        return items

    return htmltable(_analyze_dataset(stringdata, analysisf, dataaccessfunc,
                                      title=title, comparison=comparison))

def crosscorrelationmaxtable(stringdata, minlen=1, mismatchchar='_',
                             comparison='full',
                             title='Maximum crosscorrelation substring'):
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

    return htmltable(_analyze_dataset(stringdata, analysisf, dataaccessfunc,
                            title=title, comparison=comparison))

def startswithtable(stringdata, comparison='full',
                    title='Row strings starting with complete col string'):

    hc = htmlcolor_substrings

    def analysisf(s1, s2, readingframe):
        if startswith(s1, s2, readingframe):
            return ['{}&nbsp;&nbsp;{}'.format(hc(s2, s1, position=0),
                                              hc(s2, s2, position=0))]
        else:
            return ''


    def dataaccessfunc(items): return items

    return htmltable(_analyze_dataset(stringdata, analysisf, dataaccessfunc,
                            title=title, comparison=comparison))


def issubstringtable(stringdata, comparison='full', title = 'Is substring'):

    hc = htmlcolor_substrings

    def analysisf(s1, s2, readingframe):
        if issubstring(s1, s2, readingframe):
            return ['{}&nbsp;&nbsp;{}'.format(hc(s2, s1), hc(s2, s2))]
        else:
            return ''


    def dataaccessfunc(item): return item

    return htmltable(_analyze_dataset(stringdata, analysisf, dataaccessfunc,
                            title, comparison=comparison))