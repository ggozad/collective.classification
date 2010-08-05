from zope.interface import implements
from persistent import Persistent
from BTrees.IIBTree import intersection, IISet
from Products.CMFCore.utils import getToolByName
from nltk import NaiveBayesClassifier
from collective.classification.interfaces import IContentClassifier


class NounBayesClassifier(Persistent):
    """
    """
    implements(IContentClassifier)

    def __init__(self, tagger=None):
        """
        """
        self.classifier = None
        self.trainAfterUpdate = True

    def train(self):
        """
        """
        catalog = getToolByName(self, 'portal_catalog')
        presentNouns = dict()
        trainingData = []
        allNouns = catalog.uniqueValuesFor('noun_terms')
        for item in allNouns:
            presentNouns.setdefault(item, 0)

        subjectIndex = catalog._catalog.getIndex('Subject')
        nounTermsIndex = catalog._catalog.getIndex('noun_terms')

        # The internal catalog ids of the objects
        # that have noun terms in the catalog
        nounTermIndexIds = IISet(nounTermsIndex._unindex.keys())

        # The internal catalog ids of the objects
        # that have subjects in the catalog
        subjectIndexIds = IISet(subjectIndex._unindex.keys())
        commonIds = intersection(subjectIndexIds, nounTermIndexIds)

        for cid in commonIds:
            nounPresence = presentNouns.copy()
            nouns = nounTermsIndex._unindex[cid]
            tags = subjectIndex._unindex[cid]
            for noun in nouns:
                nounPresence[noun] = 1
            for tag in tags:
                trainingData.append((nounPresence, tag, ))
        if trainingData:
            self.classifier = NaiveBayesClassifier.train(trainingData)

    def classify(self, doc_id):
        """
        """
        if not self.classifier:
            return []
        presentNouns = dict()
        catalog = getToolByName(self, 'portal_catalog')
        allNouns = catalog.uniqueValuesFor('noun_terms')
        for item in allNouns:
            presentNouns.setdefault(item, 0)

        results = catalog.unrestrictedSearchResults(UID=doc_id)
        if not results:
            return []
        importantNouns = results[0]['noun_terms']
        for noun in importantNouns:
            if noun in presentNouns.keys():
                presentNouns[noun] = 1
        return self.classifier.classify(presentNouns)

    def probabilityClassify(self, doc_id):
        """
        """
        if not self.classifier:
            return []
        presentNouns = dict()
        catalog = getToolByName(self, 'portal_catalog')
        allNouns = catalog.uniqueValuesFor('noun_terms')
        for item in allNouns:
            presentNouns.setdefault(item, 0)

        results = catalog.unrestrictedSearchResults(UID=doc_id)
        if not results:
            return []
        importantNouns = results[0]['noun_terms']
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
                return cpdist[l, fname].prob(fval)
            labels = sorted([l for l in self.classifier._labels
                             if fval in cpdist[l, fname].samples()],
                            key=labelprob)
            if len(labels) == 1:
                continue
            l0 = labels[0]
            l1 = labels[-1]
            if cpdist[l0, fname].prob(fval) == 0:
                ratio = 'INF'
            else:
                ratio = '%8.1f' % (cpdist[l1, fname].prob(fval) /
                                   cpdist[l0, fname].prob(fval))
            result.append((fname, bool(fval), l1, l0, ratio))
        return result

    def tags(self):
        if not self.classifier:
            return []
        return self.classifier.labels()
