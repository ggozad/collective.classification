from persistent import Persistent
from persistent.mapping import PersistentMapping
from BTrees.OOBTree import OOSet, union
from zope.interface import implements
from nltk.metrics import ranks_from_scores
from nltk import NaiveBayesClassifier
from plone.memoize import instance

from qi.kb.classification.classifiers.npextractor import NPExtractor
from qi.kb.classification.interfaces import IContentClassifier

class NounBayesClassifier(Persistent):
    """
    """
    implements(IContentClassifier)
    
    def __init__(self,tagger=None,noNounRanksToKeep = 10):
        """
        """
        self.noNounRanksToKeep = noNounRanksToKeep
        self.trainingSet = PersistentMapping()
        self.allNouns = OOSet()
        self.classifier = None
        self.extractor = NPExtractor(tagger=tagger)

    def _extractImportantNouns(self,text):
        nounDict = self.extractor.extract(text)[0]
        importantNouns = []
        for (noun,score) in ranks_from_scores(nounDict.items()):
            if score < self.noNounRanksToKeep:
                importantNouns.append(noun)
        return importantNouns
        
    def addTrainingDocument(self,doc_id,text,tags):
        """
        """
        importantNouns = self._extractImportantNouns(text)
        if importantNouns:
            self.trainingSet[doc_id] = (importantNouns,tags,)
            self.allNouns = union(self.allNouns,OOSet(importantNouns))
        
    def train(self):
        """
        """
        trainingData = []
        presentNouns = dict()
        for item in self.allNouns:
            presentNouns.setdefault(item,0)
        
        for (nouns,tags) in self.trainingSet.values():
            nounPresence = presentNouns.copy()
            for noun in nouns:
                nounPresence[noun] = 1
            for tag in tags:
                trainingData.append((nounPresence,tag,))
        if trainingData:
            self.classifier = NaiveBayesClassifier.train(trainingData)

    @instance.memoize
    def classify(self,text):
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
    