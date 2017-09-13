from __future__ import print_function
import yaml

__all__ = ['read_stringdata', 'StringData']


class StringData(object):

    def __init__(self, strings, readingframe=1, stringcategories=None,
                 labelcolors=None, tokendurations=None, isiduration=None):

        strings = self._checkstrings(strings)
        self.stringdict = {l: s for d in strings for l, s in d.items()}
        self.stringlabels = [l for d in strings for l, s in d.items()]
        self.strings = [s for d in strings for l, s in d.items()]
        self.readingframe = readingframe

        self.stringcategories = {} if stringcategories is None else stringcategories
        self.tokendurations = tokendurations
        self.isiduration = isiduration
        labelcolors = {} if labelcolors is None else labelcolors
        self.stringlabelcolors = {}
        for category, color in labelcolors.items():
            for sl in self.stringcategories[category]:
                self.stringlabelcolors[sl] = color
        for label, string in self.stringdict.items():
            if label not in self.stringlabelcolors:
                self.stringlabelcolors[label] = 'black'
        if 'All' not in self.stringcategories:
            l = self.stringlabels
            self.stringcategories.update({'All': l})

    def _checkstrings(self, strings):
        """
        Makes sure that 'strings' is a list of dicts. If it is just a
        sequence of strings, it will return a list with dicts in which keys
        that are identical to the strings.

        """
        return [si if isinstance(si, dict) else {si: si}
                for si in strings]

    def __str__(self):
        stringlabels = self.stringcategories['All']
        maxlabellen = 0
        for stringlabel in stringlabels:
            maxlabellen = max(maxlabellen, len(stringlabel))
        lines = ['All:\n']
        for sl in stringlabels:
            s = self.stringdict[sl]
            lines.append(
                '    {:<{fill}}: {}\n'.format(sl, s, fill=maxlabellen + 1))
        lines.append('\n')
        for category, stringlabels in self.stringcategories.items():
            if not category == 'All':
                lines.append('{}: [{}]\n'.format(category,
                                                 (', '.join(stringlabels))))
                lines.append('\n')
        return ''.join(lines)

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

