import numpy
from operator import indexOf
from zope.interface import implements
from zope.component import getUtility
from nltk.cluster import KMeansClusterer
#from nltk.cluster.util import euclidean_distance, cosine_distance
from collective.classification.classifiers.utils import pearson
from collective.classification.interfaces import INounPhraseStorage
from collective.classification.interfaces import IContentClusterer
class KMeans(object):
    """
    """
    
    implements(IContentClusterer)

    def clusterize(self,noClusters,noNouranksToKeep,**kwargs):
        """
        """
        storage = getUtility(INounPhraseStorage)
        docids = storage.rankedNouns.keys()
        docnouns = []
        allNouns = set()
        vectors = []

        for key in docids:
            importantNouns = storage.getNounTerms(
                key,
                noNouranksToKeep)
            docnouns.append(importantNouns)
            allNouns = allNouns.union(importantNouns)

        for nouns in docnouns:
            vector = [(noun in nouns and 1 or 0) for noun in allNouns]
            vectors.append(numpy.array(vector))

        clusterer = KMeansClusterer(noClusters,pearson,**kwargs)
        clusters = clusterer.cluster(vectors,True)

        result = {}
        for i in range(noClusters):
            result[i] = []
        for docid in docids:
            index = indexOf(docids,docid)
            result[clusters[index]] = result[clusters[index]] + [docid]
        return result