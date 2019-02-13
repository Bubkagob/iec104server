import unittest
from os import listdir
from os.path import dirname


SUBPACKAGE = 'py60870server'


class MainCase(unittest.TestCase):
    def test_syntax(self):
        src_dir = dirname(__file__) + '/../../volcano/' + SUBPACKAGE
        files = [f[:-3] for f in listdir(src_dir) if f.endswith('.py')]
        for f in files:
            __import__('volcano.' + SUBPACKAGE + '.' + f)
            print('Successfully imported %s' % f)
