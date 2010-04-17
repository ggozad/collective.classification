from os.path import dirname, join
from collective.classification import tests

def getFile(filename):
    """ return a file object from the test data folder """
    filename = join(dirname(tests.__file__), 'data', filename)
    return open(filename, 'r')

def readData(filename):
    """ return file data """
    return getFile(filename).read()
