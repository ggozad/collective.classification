from persistent import Persistent
from zope.interface import implements
from zope.component import getUtility
from plone.memoize import ram
from nltk import RegexpParser
from nltk.chunk.util import tree2conlltags
from collective.classification.interfaces import IPOSTagger, ITokenizer, \
    ITermExtractor
from collective.classification.classifiers.utils import singularize

def _extractor_cachekey(method, self, text):
    return (self.tagger_metadata, text)

def permissiveFilter(word, occur):
    return True

class DefaultFilter(object):
    
    def __init__(self, minOccur=3):
        self.minOccur = minOccur
    
    def __call__(self, word, occur):
        return occur >= self.minOccur

class NPExtractor(Persistent):
    """
    """
    
    implements(ITermExtractor)
    
    def __init__(self):
        """
        """
        self.filter = DefaultFilter()
        self.tokenizer = getUtility(ITokenizer,
            name="collective.classification.tokenizers.NLTKTokenizer")
        self.tagger = getUtility(IPOSTagger,
                name="collective.classification.taggers.PennTreebankTagger")
        self.tagger_metadata = {'type':'Pen TreeBank','categories':[]}
        self.np_grammar = r"""
            NP: {<JJ>*<NN>}         # chunk determiners, adjectives and nouns
                {<NNP>+}            # chunk proper nouns
                """
        self.np_finder = RegexpParser(self.np_grammar)
    
    def _add(self,norm, terms):
        terms.setdefault(norm, 0)
        terms[norm] += 1
    
    @ram.cache(_extractor_cachekey)
    def extract(self,text):
        """
        """
        tokens = self.tokenizer.tokenize(text)
        tagged_terms = self.tagger.tag(tokens)
        terms = {}
        np_terms = {}
        
        noun_phrases = [
            node
            for node in self.np_finder.parse(tagged_terms)
            if not isinstance(node,tuple)]
        
        for node in noun_phrases:
            coll_tag = tree2conlltags(node)
            if len(coll_tag) > 1:
                mterm = [
                    term.lower()
                    for (term,tag,temp) in coll_tag
                    if len(term)>1
                    ]
                
                mterm = ' '.join(mterm)
                self._add(mterm,np_terms)
            for (term,tag,temp) in coll_tag:
                if tag.startswith('N') and len(term)>1:
                    if tag in ['NNS','NNPS']:
                        term = singularize(term)
                    self._add(term.lower(),terms)
        
        for term in terms.keys():
            if not self.filter(term,terms[term]):
                del terms[term]
        
        for term in np_terms.keys():
            if not self.filter(term,np_terms[term]):
                del np_terms[term]
        
        return (terms,np_terms)
    
    def setTagger(self,tagger,tagger_metadata={}):
        self.tagger = tagger
        if not tagger_metadata:
            self.tagger_metadata['type']='unknown'
        else:
            self.tagger_metadata = tagger_metadata
