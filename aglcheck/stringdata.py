from __future__ import print_function
import yaml

__all__ = ['read_stringdata', 'StringData']


class StringData(object):

    def __init__(self, strings, readingframe=1, comparisons=None,
                 labelcolors=None, subgroups=None, tokendurations=None,
                 isiduration=None):

        strings = self._checkstrings(strings)

        self.stringdict = {l: s for d in strings for l, s in d.items()}
        self.stringlabels = [l for d in strings for l, s in d.items()]
        self.strings = [s for d in strings for l, s in d.items()]
        self.readingframe = readingframe
        self.comparisons = {} if comparisons is None else comparisons
        self.labelcolors = {} if labelcolors is None else labelcolors
        self.subgroups = {} if subgroups is None else subgroups
        self.tokendurations = tokendurations
        self.isiduration = isiduration
        if 'full' not in self.comparisons:
            l = self.stringlabels
            self.comparisons.update({'full': [{'strings_a': l}, {'strings_b': l}]})

    def _checkstrings(self, strings):
        """
        Makes sure that 'strings' is a list of dicts. If it is just a
        sequence of strings, it will return a list with dicts in which keys
        that are identical to the strings.

        """
        return [si if isinstance(si, dict) else {si: si}
                for si in strings]

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
    return StringData(**d)

