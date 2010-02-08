from operator import itemgetter
from zope.interface import implements
from persistent import Persistent
from persistent.mapping import PersistentMapping
from BTrees.OOBTree import OOSet, union
from nltk.metrics import ranks_from_scores
from plone.memoize import instance
from qi.kb.classification.classifiers.npextractor import NPExtractor
from qi.kb.classification.interfaces import INounPhraseStorage

class NounPhraseStorage(Persistent):
    """A storage utility to keep noun-phrases in the ZODB.
    """
    
    implements(INounPhraseStorage)
    
    def __init__(self,tagger=None,noNounRanksToKeep = 10):
        """
        """
        self.noNounRanksToKeep = noNounRanksToKeep
        self.rankedNouns = PersistentMapping()
        self.rankedNPs = PersistentMapping()
        self.extractor = NPExtractor(tagger=tagger)
        self.allNouns = OOSet()

    def _scoresToRanks(self,rankdict):
        scored_items = sorted(rankdict.items(),key=itemgetter(1),reverse=True) 
        ranked_items = [
            ranked_item 
            for ranked_item in 
            ranks_from_scores(scored_items)]
        return ranked_items

    def addDocument(self,doc_id,text):
        """
        """
        (noun_scores,noun_phrase_scores) = self.extractor.extract(text)
        if noun_scores:
            ranked_nouns = self._scoresToRanks(noun_scores)
            self.rankedNouns[doc_id] = ranked_nouns
            
            importantNouns = []
            for (noun,score) in ranked_nouns:
                if score < self.noNounRanksToKeep:
                    importantNouns.append(noun)
            self.allNouns = union(self.allNouns,OOSet(importantNouns))
            
        if noun_phrase_scores:
            ranked_nps = self._scoresToRanks(noun_phrase_scores)
            self.rankedNPs[doc_id] = ranked_nps
