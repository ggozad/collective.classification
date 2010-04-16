from operator import itemgetter
from zope.interface import implements
from zope.component import getUtility
from persistent import Persistent
from persistent.mapping import PersistentMapping
from persistent.list import PersistentList
from nltk.metrics import ranks_from_scores
from collective.classification.interfaces import INounPhraseStorage, \
    ITermExtractor

class NounPhraseStorage(Persistent):
    """A storage utility to keep noun-phrases in the ZODB.
    """
    
    implements(INounPhraseStorage)

    def __init__(self):
        """
        """
        self.rankedNouns = PersistentMapping()
        self.rankedNPs = PersistentMapping()
        self.friendlyTypes = PersistentList()

    def _scoresToRanks(self,rankdict):
        """
        """
        scored_items = sorted(rankdict.items(),key=itemgetter(1),reverse=True)
        ranked_items = [
            ranked_item
            for ranked_item in
            ranks_from_scores(scored_items)]
        return ranked_items

    def addDocument(self,doc_id,text,locale='en'):
        """
        """
        extractor = getUtility(ITermExtractor)
        (noun_scores,noun_phrase_scores) = extractor.extract(text,locale)
        if noun_scores:
            ranked_nouns = self._scoresToRanks(noun_scores)
            self.rankedNouns[doc_id] = ranked_nouns
        if noun_phrase_scores:
            ranked_nps = self._scoresToRanks(noun_phrase_scores)
            self.rankedNPs[doc_id] = ranked_nps

    def removeDocument(self,doc_id):
        """
        """
        if self.rankedNouns.has_key(doc_id):
            del self.rankedNouns[doc_id]
        if self.rankedNPs.has_key(doc_id):
            del self.rankedNPs[doc_id]            

    def _derankTerms(self,rankedTerms):
        return [term for (term,rank) in rankedTerms]

    def getRankedTerms(self,doc_id,ranksToKeep=0):
        """
        """
        ranked_nouns = self.rankedNouns.get(doc_id,[])
        ranked_nps = self.rankedNPs.get(doc_id,[])
        if ranksToKeep:
            ranked_nouns = [
                (noun,score)
                for (noun,score) in ranked_nouns
                if score < ranksToKeep]
            ranked_nps = [
                (np,score)
                for (np,score) in ranked_nps
                if score < ranksToKeep]
        return (ranked_nouns,ranked_nps)

    def getTerms(self,doc_id,ranksToKeep=0):
        (ranked_nouns,ranked_nps) = self.getRankedTerms(doc_id,ranksToKeep)
        ranked_nouns = self._derankTerms(ranked_nouns)
        ranked_nps = self._derankTerms(ranked_nps)
        return (ranked_nouns,ranked_nps)

    def getRankedNounTerms(self,doc_id,ranksToKeep=0):
        """
        """
        ranked_nouns = self.rankedNouns.get(doc_id,[])
        if ranksToKeep:
            ranked_nouns = [
                (noun,score)
                for (noun,score) in ranked_nouns
                if score < ranksToKeep]
        return ranked_nouns

    def getRankedNPTerms(self,doc_id,ranksToKeep=0):
        """
        """
        ranked_nps = self.rankedNPs.get(doc_id,[])
        if ranksToKeep:
            ranked_nps = [
                (np,score)
                for (np,score) in ranked_nps
                if score < ranksToKeep]
        return ranked_nps

    def getNounTerms(self,doc_id,ranksToKeep=0):
        ranked_nouns = self.getRankedNounTerms(doc_id,ranksToKeep)
        return self._derankTerms(ranked_nouns)

    def getNPTerms(self,doc_id,ranksToKeep=0):
        ranked_nps = self.getRankedNPTerms(doc_id,ranksToKeep)
        return self._derankTerms(ranked_nps)

    def clear(self):
        """Wipes the storage
        """
        self.rankedNouns.clear()
        self.rankedNPs.clear()