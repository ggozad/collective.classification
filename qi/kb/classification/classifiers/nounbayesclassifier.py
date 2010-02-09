from zope.component import getUtility
from zope.interface import implements
from persistent import Persistent
from persistent.mapping import PersistentMapping
from BTrees.OOBTree import OOSet, union
from nltk import NaiveBayesClassifier
from plone.memoize import instance
from qi.kb.classification.interfaces import IContentClassifier
from qi.kb.classification.interfaces import INounPhraseStorage

class NounBayesClassifier(Persistent):
    """
    """
    implements(IContentClassifier)
    
    def __init__(self,tagger=None,noNounRanksToKeep = 10):
        """
        """
        self.noNounRanksToKeep = noNounRanksToKeep
        self.trainingDocs = PersistentMapping()
        self.allNouns = OOSet()

        self.classifier = None
        self.trainAfterUpdate = False

    def addTrainingDocument(self,doc_id,tags):
        """
        """
        storage = getUtility(INounPhraseStorage)        
        importantNouns = storage.getTerms(doc_id,self.noNounRanksToKeep)[0]
        
        self.trainingDocs[doc_id] = (importantNouns,tags)
        self.allNouns = union(self.allNouns,OOSet(importantNouns))
        
    def train(self):
        """
        """
        presentNouns = dict()        
        trainingData = []
        
        for item in self.allNouns:
            presentNouns.setdefault(item,0)
        
        for (nouns,tags) in self.trainingDocs.values():
            nounPresence = presentNouns.copy()
            for noun in nouns:
                nounPresence[noun] = 1
            for tag in tags:
                trainingData.append((nounPresence,tag,))
        if trainingData:
            self.classifier = NaiveBayesClassifier.train(trainingData)

    def classify(self,doc_id):
        """
        """
        if not self.classifier:
            return []
        
        presentNouns = dict()
        for item in self.allNouns:
            presentNouns.setdefault(item,0)

        importantNouns = self.getTerms(doc_id)[0]
        for noun in importantNouns:
            if noun in presentNouns.keys():
                presentNouns[noun] = 1
        return self.classifier.classify(presentNouns)

    @instance.memoize
    def probabilityClassify(self,text):
        """
        """
        if not self.classifier:
            return []
        presentNouns = dict()
        for item in self.allNouns:
            presentNouns.setdefault(item,0)

        importantNouns = self._extractImportantNouns(text)
        for noun in importantNouns:
            if noun in presentNouns.keys():
                presentNouns[noun] = 1
        return self.classifier.prob_classify(presentNouns)

    def clear(self):
        """Wipes the classifier's data.
        """
        self.allNouns.clear()
        self.trainingData.clear()
        
    def tags(self):
        if not self.classifier:
            return []
        return self.classifier.labels()
        