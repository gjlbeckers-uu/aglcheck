import numpy as np

__all__ = ['commonstart', 'commonstartlength', 'commonstartduration',
           'crosscorrelate', 'sharedlengthnsubstrings',
           'longestsharedsubstrings', 'longestsharedsubstringduration',
           'novellengthnsubstrings', 'samestart', 'samestart',
           'sharedsubstrings']


# Notations:
# ---------
# s1, s2, ..., sn : strings
# s1ss, s2ss, ..., snss: sharedsubstrings of s1, s2, ..., sn
# ss1, ss2, ..., ssn : sharedsubstrings


def _checkpositiveint(i):
    if not (isinstance(i, int) and (i > 0)):
        raise ValueError("i ({}) should be an int > 0".format(i))


def _checkstring(s, readingframe=1):
    if not (isinstance(s, str) and len(s) >= readingframe):
        raise TypeError("s1 and s2 should be strings with at least one "
                        "element")
    if readingframe > 1:
        if not len(s) % readingframe == 0:
            raise ValueError('string "{}" not comatible with '
                             'readingframe of {}'.format(s, readingframe))

def lengthnsubstrings(s, n, readingframe=1):
    """
    Returns a tuple of consecutive length-n substrings of s.
    
    Parameters
    ----------
    s : string
        String from which length-n substrings are generated. 
    n : positive int
        Length of the shared substrings that are considered
    readingframe : positive int, default 1
        The number of characters that make up one string token. Normally 1,
        so that, e.g. the string "abcd" has 4 tokens. However if there exist
        many tokens, these can be coded with multiple ascii symbols. E.g., if
        readingframe is 2, then "abcd" has two tokens, namely "ab" and "cd".

    Returns
    -------
    Tuple with substrings

    Examples
    --------
    >>> from aglcheck.algorithms import lengthnsubstrings
    >>> lengthnsubstrings('abcdefghi', n=4)
    ('abcd', 'bcde', 'cdef', 'defg', 'efgh', 'fghi')
    >>> lengthnsubstrings('a1a2a3c1b3b2b1', n=4, readingframe=2)
    ('a1a2a3c1', 'a2a3c1b3', 'a3c1b3b2', 'c1b3b2b1')

    """
    _checkpositiveint(readingframe)
    _checkstring(s, readingframe=readingframe)
    _checkpositiveint(n)
    # how many length-n substrings exist in in s1?
    nss1 = int(len(s) / readingframe) - n + 1
    return tuple(s[i:i + n * readingframe]
                 for i in range(0, nss1 * readingframe, readingframe))


def sharedlengthnsubstrings(s1, s2, n, readingframe=1):
    """
    Finds length-n shared substrings of s1 in s2.

    Parameters
    ----------
    s1 : string
        String from which length-n substrings are analyzed
    s2 : string
        String within which length-n substrings of s1 are matched
    n : positive int
        Length of the shared substrings that are considered
    readingframe : positive int, default 1
        The number of characters that make up one string token. This will
        often be `1`, so that, e.g. the string "abcd" has 4 tokens. However if
        there are more tokens than can be coded in ascii symbols,
        the larger readingframes are the solution. E.g., if readingframe is 2,
        then "a1b1" has two tokens, namely "a1" and "b1".

    Returns
    -------
    Tuple with hits. Each hit is a two-tuple, containing a
    substring match and a two-tuple of the positions where the shared 
    substrings occur in s1 and s2. Note that the positions refer to the
    token strings, and not python strings. They take into account the reading
    frame.

    Examples
    --------
    >>> from aglcheck.algorithms import sharedlengthnsubstrings
    >>> sharedlengthnsubstrings('abcdefg', 'cdfgbcd', n=2)
    (('bc', ((1, 4),)), ('cd', ((2, 0), (2, 5))), ('fg', ((5, 2),)))
    >>> sharedlengthnsubstrings('a1a2c1b2b1', 'c1b2b1a1a2', n=2, readingframe=2)
    (('a1a2', ((0, 3),)), ('c1b2', ((2, 0),)), ('b2b1', ((3, 1),)))

    """

    _checkpositiveint(readingframe)
    _checkstring(s1, readingframe=readingframe)
    _checkstring(s2, readingframe=readingframe)
    _checkpositiveint(n)
    s1ss = lengthnsubstrings(s1, n=n, readingframe=readingframe)
    matches = []
    for pos, substring in enumerate(s1ss):
        positions = []
        for i in range(0, len(s2), readingframe):
            if substring == s2[i:i + n * readingframe]:
                positions.append((pos, int(i/readingframe)))
        if len(positions) > 0:
            matches.append((substring, tuple(positions)))
    return tuple(matches)


def sharedsubstrings(s1, s2, readingframe=1):
    """
    Finds all possible shared substrings of s1 in s2.

    Parameters
    ----------
    s1 : string
        String from which length-n substrings are generated.
    s2 : string
        String within which length-n substrings of s1 are matched.
    readingframe : positive int, default 1
        The number of characters that make up one string token. Normally 1,
        so that, e.g. the string "abcd" has 4 tokens. However if there exist
        many tokens, these can be coded with multiple ascii symbols. E.g., if
        readingframe is 2, then "abcd" has two tokens, namely "ab" and "cd".

    Returns
    -------
    Tuple with hits. Each hit is a two-tuple, containing a
    substring match and the number of times it occurs.
    
    Examples
    --------
    >>> from aglcheck.algorithms import sharedsubstrings
    >>> sharedsubstrings('abcd', 'cdecd')
    ((('c', ((2, 0), (2, 3))), ('d', ((3, 1), (3, 4)))),
     (('cd', ((2, 0), (2, 3))),))
    >>> sharedsubstrings('a1a2', 'a2a3a1a2', readingframe=2)
    ((('a1', ((0, 2),)), ('a2', ((1, 0), (1, 3)))), (('a1a2', ((0, 2),)),))
     
    """

    matches = [sharedlengthnsubstrings(s1, s2, n, readingframe)
               for n in range(1, len(s1) + 1)]
    # remove empty 'matches'
    return tuple(match for match in matches if match)


def longestsharedsubstrings(s1, s2, readingframe=1):
    """
    Finds longest shared substrings of s1 in s2. If there are multiple
    matches, return every match.

    Parameters
    ----------
    s1 : string
        String from which length-n substrings are generated.
    s2 : string
        String within which length-n substrings of s1 are matched.
    readingframe : positive int, default 1
        The number of characters that make up one string token. Normally 1,
        so that, e.g. the string "abcd" has 4 tokens. However if there exist
        many tokens, these can be coded with multiple ascii symbols. E.g., if
        readingframe is 2, then "abcd" has two tokens, namely "ab" and "cd".

    Returns
    -------
    Tuple with hits. Each hit is a two-tuple, containing a
    substring match and the positions where it occurs.
    
    Examples
    --------
    >>> from aglcheck.algorithms import longestsharedsubstrings
    >>> longestsharedsubstrings('acd', 'cdacdeacd')
    (('acd', ((0, 2), (0, 6))),)
    >>> longestsharedsubstrings('acde', 'cdbcdeacd')
    (('acd', ((0, 6),)), ('cde', ((1, 3),)))
    >>> longestsharedsubstrings('a1a2', 'a2a3a1a2a1', readingframe=2)
    (('a1a2', ((0, 2),)),)
    
    """
    for n in range(len(s1)//readingframe, 0, -1):
        matches = sharedlengthnsubstrings(s1, s2, n, readingframe)
        if matches:
            return matches
    return ()


def longestsharedsubstringduration(s1, s2, tokendurations, isiduration,
                                   readingframe=1):
    durations = [0.]
    for s, positions in longestsharedsubstrings(s1=s1, s2=s2,
                                                readingframe=readingframe):
        elements = [s[i:i + readingframe] for i in
                    range(0, len(s), readingframe)]
        sounddur = sum([tokendurations[el] for el in elements])
        durations.append(sounddur + (len(elements) - 1) * isiduration)
    return float(np.max(durations))


def novellengthnsubstrings(s1, s2, n, readingframe=1):
    """
    Finds length-n shared substrings of s1 that are absent in s2.

    Parameters
    ----------
    s1 : string
        String from which length-n substrings are generated.
    s2 : string
        String within which length-n substrings of s1 are matched
    n : positive int
        Length of the shared substrings that are considered
    readingframe : positive int, default 1
        The number of characters that make up one string token. Normally 1,
        so that, e.g. the string "abcd" has 4 tokens. However if there exist
        many tokens, these can be coded with multiple ascii symbols. E.g., if
        readingframe is 2, then "abcd" has two tokens, namely "ab" and "cd".

    Returns
    -------
    Tuple with hits. Each hit is a two-tuple, containing a 
    substring mismatch and the position where the shared 
    substrings occurs in s1. Note that the positions refer to the 
    python strings, and do not take into account the reading frame.

    """

    _checkpositiveint(readingframe)
    _checkstring(s1, readingframe=readingframe)
    _checkstring(s2, readingframe=readingframe)
    _checkpositiveint(n)
    # which length-n substrings exist in in s1?
    s1ss = lengthnsubstrings(s1, n=n, readingframe=readingframe)
    s2ss = set(lengthnsubstrings(s2, n=n, readingframe=readingframe))
    return tuple((ss, pos) for pos, ss in enumerate(s1ss) if ss not in s2ss)



def commonstart(s1, s2, readingframe=1):
    """
    Returns the substring that s1 and s2 share from the beginning.

    """
    # check if parameters make sense
    _checkstring(s1, readingframe=readingframe)
    _checkstring(s2, readingframe=readingframe)
    _checkpositiveint(readingframe)

    i = sum([s2.startswith(s1[:i]) for i in
             range(readingframe, len(s1) + 1, readingframe)])
    return s1[:i * readingframe]


def commonstartlength(s1, s2, readingframe=1):
    """
    Counts the length of the substring that both s1 and s2 start with.

    """
    return len(commonstart(s1=s1, s2=s2,
                           readingframe=readingframe)) // readingframe


def commonstartduration(s1, s2, tokendurations, isiduration, readingframe=1):
    s = commonstart(s1=s1, s2=s2, readingframe=readingframe)
    elements = [s[i:i + readingframe] for i in range(0, len(s), readingframe)]
    sounddur = np.sum([tokendurations[el] for el in elements])
    if len(elements) > 0:
        return sounddur + (len(elements) - 1) * isiduration
    else:
        return 0.


def crosscorrelate(s1, s2, readingframe=1, full=True):
    _checkstring(s1, readingframe=readingframe)
    _checkstring(s2, readingframe=readingframe)
    _checkpositiveint(readingframe)
    if readingframe > 1:
        s1 = [s1[i:i + readingframe] for i in range(0, len(s1), readingframe)]
        s2 = [s2[i:i + readingframe] for i in range(0, len(s2), readingframe)]
    sa1 = np.array(list(s1))
    sa2 = np.zeros(2 * len(s1) + len(s2) - 2, dtype=sa1.dtype)
    sa2[sa1.size - 1:sa1.size + len(s2) - 1] = list(s2)
    nsteps = len(sa2) - len(sa1)
    ccp = [(sa1 == sa2[i:i + sa1.size]) for i in range(nsteps + 1)]
    ccs = [[item if isequal else '' for (isequal, item) in zip(cc, sa1)] for cc
           in ccp]
    ccf = np.array([(sa1 == sa2[i:i + sa1.size]).sum()
                    for i in range(nsteps + 1)])

    if full:
        return ccf, ccs
    else:
        return ccf[sa1.size - 1:-(sa1.size - 1)], \
               ccs[sa1.size - 1:-(sa1.size - 1)]


def issubstring(s1, s2, *args, **kwargs):
    """Is s1 a substring of s2"""
    return s2.count(s1) > 0

# we need the next function even though it seems redundant, because
# the 'readingframe' parameter may be supplied by other functions
def startswith(s1, s2, *args, **kwargs):
    return s1.startswith(s2)


def samestart(s1, s2, n, readingframe=1):
    return s1[:n * readingframe] == s2[:n * readingframe]


def levenshtein(s1, s2, readingframe=1):
    """
    Code adapted from: https://en.wikibooks.org/wiki/Algorithm_Implementation
    /Strings/Levenshtein_distance#Python

    """
    _checkstring(s1, readingframe=readingframe)
    _checkstring(s2, readingframe=readingframe)
    _checkpositiveint(readingframe)
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    if readingframe > 1:
        s1 = [s1[i:i + readingframe] for i in range(0, len(s1), readingframe)]
        s2 = [s2[i:i + readingframe] for i in range(0, len(s2), readingframe)]
    previous_row = range(0, len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]
