from zope.component import getUtility
from nltk.corpus import brown
from collective.classification.tests.base import ClassificationTestCase
from collective.classification.classifiers.clustering import KMeans
from collective.classification.interfaces import INounPhraseStorage

class TestKMeansClustering(ClassificationTestCase):
    """Test the KMeans clusterer.
    """

    def test_clusterer(self):
        """Here we take 10 documents categorized as 'government' and
        'mystery' from the brown corpus, and perform k-means clustering on
        these. Optimally we would like the clusterer to divide them in two
        clusters.
        The clusterer generates clusters depending on random initial
        conditions, so the result can be different in different test runs.
        In order to account for that that we run a lot of iterations
        (50) which hopefully will generate a good result. The success
        condition is that a max of  1 out of 10 documents will fall in the 
        wrong cluster.
        """

        storage = getUtility(INounPhraseStorage)
        clusterer = KMeans()
        government_ids = brown.fileids(categories='government')[:10]        
        mystery_ids = brown.fileids(categories='mystery')[:10]

        for articleid in government_ids:
            text = " ".join(brown.words(articleid))
            storage.addDocument(articleid,text)

        for articleid in mystery_ids:
            text = " ".join(brown.words(articleid))
            storage.addDocument(articleid,text)
        result = clusterer.clusterize(2,20,repeats=50)
        cluster1 = set(result[0])
        missed = min(len(cluster1-set(government_ids)),
                     len(cluster1-set(mystery_ids)))
        self.failUnless(missed<2)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestKMeansClustering))
    return suite