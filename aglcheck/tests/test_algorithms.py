from unittest import TestCase

from aglcheck.algorithms import sharedlengthnsubstrings, sharedsubstrings, \
    longestsharedsubstrings, novellengthnsubstrings

class TestLengthnSubstrings(TestCase):

    def test_fullpartsingleresult(self):
        s1 = "bc"
        s2 = "abcde"
        ss = sharedlengthnsubstrings(s1=s1, s2=s2, n=2, readingframe=1)
        self.assertEqual(ss, ((('bc'),((0, 1),)),))

    def test_fullpartsingleresultstart(self):
        s1 = "ab"
        s2 = "abcde"
        ss = sharedlengthnsubstrings(s1=s1, s2=s2, n=2, readingframe=1)
        self.assertEqual(ss, ((('ab'), ((0, 0),)),))

    def test_fullpartsingleresultend(self):
        s1 = "de"
        s2 = "abcde"
        ss = sharedlengthnsubstrings(s1=s1, s2=s2, n=2, readingframe=1)
        self.assertEqual(ss, ((('de'), ((0, 3),)),))

    def test_partpartsingleresult(self):
        s1 = "fbcg"
        s2 = "abcde"
        ss = sharedlengthnsubstrings(s1=s1, s2=s2, n=2, readingframe=1)
        self.assertEqual(ss, ((('bc'), ((1, 1),)),))

    def test_partpartsingleresultstart(self):
        s1 = "fabg"
        s2 = "abcde"
        ss = sharedlengthnsubstrings(s1=s1, s2=s2, n=2, readingframe=1)
        self.assertEqual(ss, ((('ab'), ((1, 0),)),))

    def test_partpartsingleresultend(self):
        s1 = "fdeg"
        s2 = "abcde"
        ss = sharedlengthnsubstrings(s1=s1, s2=s2, n=2, readingframe=1)
        self.assertEqual(ss, ((('de'), ((1, 3),)),))

    def test_partfullsingleresult(self):
        s1 = "fbcg"
        s2 = "bc"
        ss = sharedlengthnsubstrings(s1=s1, s2=s2, n=2, readingframe=1)
        self.assertEqual(ss, ((('bc'), ((1, 0),)),))

    def test_partfullsingleresultstart(self):
        s1 = "abgf"
        s2 = "ab"
        ss = sharedlengthnsubstrings(s1=s1, s2=s2, n=2, readingframe=1)
        self.assertEqual(ss, ((('ab'), ((0, 0),)),))

    def test_partfullsingleresultend(self):
        s1 = "fgde"
        s2 = "de"
        ss = sharedlengthnsubstrings(s1=s1, s2=s2, n=2, readingframe=1)
        self.assertEqual(ss, ((('de'), ((2, 0),)),))

    def test_doubleresult(self):
        s1 = "fdeg"
        s2 = "abcdedef"
        ss = sharedlengthnsubstrings(s1=s1, s2=s2, n=2, readingframe=1)
        self.assertEqual(ss, ((('de', ((1, 3), (1, 5),)),)))

    def test_fullpartdoubleresult(self):
        s1 = "de"
        s2 = "abcdedef"
        ss = sharedlengthnsubstrings(s1=s1, s2=s2, n=2, readingframe=1)
        self.assertEqual(ss, ((('de', ((0, 3), (0, 5),)),)))

    def test_partfulldoubleresult(self):
        s1 = "fdeg"
        s2 = "dede"
        ss = sharedlengthnsubstrings(s1=s1, s2=s2, n=2, readingframe=1)
        self.assertEqual(ss, ((('de', ((1, 0), (1, 2),)),)))

    def test_readingframe2(self):
        s1 = "cdefgi"
        s2 = "abcdefgh"
        ss = sharedlengthnsubstrings(s1=s1, s2=s2, n=2, readingframe=2)
        self.assertEqual(ss, ((('cdef', ((0, 1),)),)))


class TestSubstrings(TestCase):

    def test_result(self):
        s1 = 'bc'
        s2 = 'abcde'
        ss = sharedsubstrings(s1=s1, s2=s2, readingframe=1)
        self.assertEqual(ss, ((('b', ((0, 1),)),
                               ('c', ((1, 2),))),
                              (('bc', ((0, 1),)),)))


class TestLongestSubstrings(TestCase):

    def test_singleresult(self):
        s1 = 'bc'
        s2 = 'abcde'
        ss = longestsharedsubstrings(s1=s1, s2=s2, readingframe=1)
        self.assertEqual(ss, ((('bc', ((0, 1),)),)))

    def test_doubleresult(self):
        s1 = 'bcdabc'
        s2 = 'abcde'
        ss = longestsharedsubstrings(s1=s1, s2=s2, readingframe=1)
        self.assertEqual(ss, (('bcd', ((0, 1),)), ('abc', ((3, 0),))))


class TestNovelLengthnSubstrings(TestCase):

    def test_singleresultn1(self):
        s1 = 'abc'
        s2 = 'abd'
        ss = novellengthnsubstrings(s1, s2, n=1, readingframe=1)
        self.assertEqual(ss, (('c', 2),))

    def test_singleresultn2(self):
        s1 = 'abc'
        s2 = 'abd'
        ss = novellengthnsubstrings(s1, s2, n=2, readingframe=1)
        self.assertEqual(ss, (('bc', 1),))

    def test_doubleresultn1(self):
        s1 = 'abc'
        s2 = 'ade'
        ss = novellengthnsubstrings(s1, s2, n=1, readingframe=1)
        self.assertEqual(ss, (('b', 1),('c', 2)))

    def test_doubleresultn2(self):
        s1 = 'abc'
        s2 = 'ade'
        ss = novellengthnsubstrings(s1, s2, n=2, readingframe=1)
        self.assertEqual(ss, (('ab', 0),('bc', 1)))

    def test_singleresultn2readingframe2(self):
        s1 = 'abcdefghij'
        s2 = 'azcdefghij'
        ss = novellengthnsubstrings(s1, s2, n=2, readingframe=2)
        self.assertEqual(ss, (('abcd', 0),))

    def test_doubleresultn2readingframe2(self):
        s1 = 'abcdefghij'
        s2 = 'abcdfeghij'
        ss = novellengthnsubstrings(s1, s2, n=2, readingframe=2)
        self.assertEqual(ss, (('cdef', 1), ('efgh', 2)))
