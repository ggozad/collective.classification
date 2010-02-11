from nltk.corpus import brown
from zope.component import getUtility
from qi.kb.classification.tests.base import ClassificationTestCase
from qi.kb.classification.classifiers.clustering \
    import KMeans
from qi.kb.classification.interfaces import IPOSTagger
from qi.kb.classification.interfaces import INounPhraseStorage


class TestKMeansClustering(ClassificationTestCase):
    """Test the Naive Bayes document classifier using only the most frequent
    nouns as input. As sample test we train the classifier with a few articles
    from nltk's brown corpus categorised as 'editorial'  and a few others 
    categorised as 'hobbies'. Then, we test the classifier with 15 additional 
    documents, getting 12/15 right.
    """
    
    def afterSetUp(self):
        tagged_sents =  brown.tagged_sents(
            categories=['editorial','hobbies'])
        self.tagger = getUtility(IPOSTagger,
            name="qi.kb.classification.taggers.NgramTagger")
        self.tagger.train(tagged_sents)
        
    def test_extractor(self):
        """
        """
        clusterer = KMeans()
        storage = getUtility(INounPhraseStorage) 
        editorial_ids = brown.fileids(categories='editorial')[:25]        
        hobbies_ids = brown.fileids(categories='hobbies')[:25]
        
        for articleid in editorial_ids:
            text = " ".join(brown.words(articleid))
            storage.addDocument(articleid,text)
        
        for articleid in hobbies_ids:
            text = " ".join(brown.words(articleid))
            storage.addDocument(articleid,text)

        print clusterer.clusterize(2,20,repeats=20)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestKMeansClustering))
    return suite
