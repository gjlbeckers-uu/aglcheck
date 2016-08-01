import os
from .stringdata import read_stringdata

datadir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'datafiles')

examplestringdata = [fn.rstrip('.yaml') for fn in os.listdir(datadir)]

def get_examplestringdata(name):
    return read_stringdata(os.path.join(datadir, '{}.yaml'.format(name)))

