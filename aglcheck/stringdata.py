from __future__ import print_function
import yaml

__all__ = ['read_stringdata']


class StringData(object):

    def __init__(self, stringdatadict):

        self._stringdatadict = stringdatadict
        self.stringdict = {l: s for d in stringdatadict['strings'] for l, s in
                           d.items()}
        self.stringlabels = [l for d in stringdatadict['strings'] for l, s in
                             d.items()]
        self.strings = [s for d in stringdatadict['strings'] for l, s in
                        d.items()]
        self.readingframe = stringdatadict.get('readingframe', 1)
        self.comparisons = stringdatadict.get('comparisons', {})
        self.labelcolors = stringdatadict.get('labelcolors', {})
        self.subgroups = stringdatadict.get('subgroups', {})
        if 'full' not in self.comparisons:
            l = self.stringlabels
            self.comparisons.update({'full': [{'strings_a': l}, {'strings_b': l}]})
        for key in ('tokendurations', 'isiduration'):
            if key in stringdatadict:
                setattr(self, key, stringdatadict[key])


    def print_strings(self, comparison='full'):

        gdl = self.comparisons[comparison]
        maxkeylen = 0
        for gd in gdl:
            for gl, sl in gd.items():
                for s in sl:
                    maxkeylen = max(maxkeylen, len(s))
        lines = []
        for sd in gdl:
            for compgrouplabel, stringlabels in sd.items():
                for sl in stringlabels:
                    lines.append('{:<{fill}}: {}\n'.format(sl, self.stringdict[sl],
                                                       fill=maxkeylen + 1))
            lines.append('\n')
        print(''.join(lines))

    def __str__(self):
        return '<stringdata: {}>'.format(' '.join(self.stringlabels))

    __repr__ = __str__


def read_stringdata(filename):
    """Returns a dictionary with at least a 'strings' key. In addition it may
    contain a 'readingframe' key, a 'comparisons' key and a 'categories' key,
    and anything you defined in that file.

    """

    with open(filename, 'r') as f:
        d = yaml.load(f)
    if 'strings' not in d:
        raise ValueError("No 'strings' entry found")
    return StringData(d)

