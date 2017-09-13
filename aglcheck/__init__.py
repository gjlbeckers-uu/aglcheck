from __future__ import absolute_import
from .stringdata import read_stringdata, StringData
from ._examples import examplestringdata, get_examplestringdata
from . import algorithms
from . import compare_sets
from . import plotting
from . import htmltables

from numpy.testing import Tester
test = Tester().test
bench = Tester().bench

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
