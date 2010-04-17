from zope.component import getUtility
from zope.interface import implements
from persistent import Persistent
from persistent.mapping import PersistentMapping
from BTrees.OOBTree import OOSet, union
from nltk import NaiveBayesClassifier
from collective.classification.interfaces import IContentClassifier
from collective.classification.interfaces import INounPhraseStorage

class NounBayesClassifier(Persistent):
    """
    """
    implements(IContentClassifier)

    def __init__(self,tagger=None,noNounRanksToKeep = 20):
        """
        """
        self.noNounRanksToKeep = noNounRanksToKeep
        self.trainingDocs = PersistentMapping()
        self.allNouns = OOSet()
        
        self.classifier = None
        self.trainAfterUpdate = True

    def addTrainingDocument(self,doc_id,tags):
        """
        """
        storage = getUtility(INounPhraseStorage)
        importantNouns = storage.getNounTerms(doc_id,self.noNounRanksToKeep)
        if importantNouns and tags:
            self.trainingDocs[doc_id] = (importantNouns,tags)
            self.allNouns = union(self.allNouns,OOSet(importantNouns))
        elif self.trainingDocs.has_key(doc_id):
            del self.trainingDocs[doc_id]

    def removeTrainingDocument(self,doc_id):
        """
        """
        if self.trainingDocs.has_key(doc_id):
            del self.trainingDocs[doc_id]

    def train(self):
        """
        """
        presentNouns = dict()
        trainingData = []
        if not self.allNouns:
            storage = getUtility(INounPhraseStorage)
            for key in self.trainingDocs.keys():
                importantNouns = storage.getNounTerms(key,
                                                      self.noNounRanksToKeep)
                self.allNouns = union(self.allNouns,OOSet(importantNouns))
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
        storage = getUtility(INounPhraseStorage)
        importantNouns = storage.getNounTerms(doc_id,self.noNounRanksToKeep)
        for noun in importantNouns:
            if noun in presentNouns.keys():
                presentNouns[noun] = 1
        return self.classifier.classify(presentNouns)

    def probabilityClassify(self,doc_id):
        """
        """
        if not self.classifier:
            return []
        presentNouns = dict()
        for item in self.allNouns:
            presentNouns.setdefault(item,0)
        storage = getUtility(INounPhraseStorage)
        importantNouns = storage.getNounTerms(doc_id,self.noNounRanksToKeep)
        for noun in importantNouns:
            if noun in presentNouns.keys():
                presentNouns[noun] = 1
        return self.classifier.prob_classify(presentNouns)

    def informativeFeatures(self, n=10):
        """Determines and returns the most relevant features
        """
        if not self.classifier:
            return []
        cpdist = self.classifier._feature_probdist
        result = []
        for (fname, fval) in self.classifier.most_informative_features(n):
            def labelprob(l):
              return cpdist[l,fname].prob(fval)
            labels = sorted([l for l in self.classifier._labels
                             if fval in cpdist[l,fname].samples()],
                            key=labelprob)
            if len(labels) == 1: continue
            l0 = labels[0]
            l1 = labels[-1]
            if cpdist[l0,fname].prob(fval) == 0:
              ratio = 'INF'
            else:
              ratio = '%8.1f' % (cpdist[l1,fname].prob(fval) /
                                cpdist[l0,fname].prob(fval))
            result.append((fname, bool(fval), l1, l0, ratio))
        return result

    def clear(self):
        """Wipes the classifier's data.
        """
        self.allNouns.clear()
        self.trainingDocs.clear()

    def tags(self):
        if not self.classifier:
            return []
        return self.classifier.labels()