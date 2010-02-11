import numpy
from zope.component import getUtility
from nltk.cluster import KMeansClusterer, GAAClusterer
from nltk.cluster.util import euclidean_distance, cosine_distance
from operator import indexOf
from qi.kb.classification.classifiers.utils import pearson
from qi.kb.classification.interfaces import INounPhraseStorage

class KMeans(object):
    """
    """
    
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
        #clusterer = GAAClusterer(2)
        #clusters = clusterer.cluster(vectors, True)
        
        result = {}
        for i in range(noClusters):
            result[i] = []
        for docid in docids:
            index = indexOf(docids,docid)
            result[clusters[index]] = result[clusters[index]] + [docid]        
        return result
    