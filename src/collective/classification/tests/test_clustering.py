from nltk.corpus import brown
from collective.classification.tests.base import ClassificationTestCase
from collective.classification.classifiers.clustering import KMeans


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
        condition is that a max of 2 out of 10 documents will fall in the
        wrong cluster.
        """

        clusterer = KMeans()
        government_ids = brown.fileids(categories='government')[:10]
        mystery_ids = brown.fileids(categories='mystery')[:10]
        government_uids = []
        mystery_uids = []

        for articleid in government_ids:
            text = " ".join(brown.words(articleid))
            self.folder.invokeFactory('Document', articleid, text=text)
            government_uids.append(self.folder[articleid].UID())

        for articleid in mystery_ids:
            text = " ".join(brown.words(articleid))
            self.folder.invokeFactory('Document', articleid, text=text)
            mystery_uids.append(self.folder[articleid].UID())

        result = clusterer.clusterize(2, 50, repeats=50)
        cluster1 = set(result[0])
        missed = min(len(cluster1-set(government_uids)),
                     len(cluster1-set(mystery_uids)))
        self.failUnless(missed<=2)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestKMeansClustering))
    return suite
