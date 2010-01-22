from nltk.corpus import brown
from qi.kb.classification import tests
from os.path import dirname, join

def dump():
    """
    """
    a_ids = brown.fileids(categories='news')
    for a_id in a_ids[:25]:
        text = ""
        words = brown.words(a_id)
        text = " ".join(words)
        filename = a_id+".txt"
        filename = join(dirname(tests.__file__), 'data', filename)
        f = open(filename,"w")
        f.write(text)
        f.close