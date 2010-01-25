from nltk.corpus import brown
from zope.component import getUtility
from qi.kb.classification.tests.base import ClassificationTestCase
from qi.kb.classification.classifiers.nounbayesclassifier \
    import NounBayesClassifier
from qi.kb.classification.interfaces import IPOSTagger


class TestNounClassification(ClassificationTestCase):
    """Test the Naive Bayes document classifier using only the most frequent
    nouns as input. As sample test we train the classifier with a few articles
    from nltk's brown corpus categorised as 'editorial'  and a few others 
    categorised as 'hobbies'. Then, we test the classifier with 15 additional 
    documents, getting 12/15 right.
    """
    
    def afterSetUp(self):
        tagged_sents =  brown.tagged_sents(
            categories=['editorial','hobbies','news'])
        self.tagger = getUtility(IPOSTagger,
            name="qi.kb.termextraxt.taggers.NgramTagger")
        self.tagger.train(tagged_sents)
        
    def test_extractor(self):
        """
        """
        classifier = NounBayesClassifier(tagger=self.tagger)
        news_ids = brown.fileids(categories='news')[:25]
        editorial_ids = brown.fileids(categories='editorial')[:25]        
        hobbies_ids = brown.fileids(categories='hobbies')[:25]

        for articleid in news_ids[:20]:
            text = " ".join(brown.words(articleid))
            classifier.addTrainingDocument(articleid,text,['news'])
        
        for articleid in editorial_ids[:20]:
            text = " ".join(brown.words(articleid))
            classifier.addTrainingDocument(articleid,text,['editorial'])
        
        for articleid in hobbies_ids[:20]:
            text = " ".join(brown.words(articleid))
            classifier.addTrainingDocument(articleid,text,['hobbies'])
        classifier.train()

        self.failUnless(classifier.tags() == ['editorial','hobbies','news'])

        classificationResult = []
        for articleid in editorial_ids[20:25] + \
                        hobbies_ids[20:25] + \
                        news_ids[20:25]:
            text = " ".join(brown.words(articleid))
            classificationResult.append(classifier.classify(text))
        self.failUnless(classificationResult == 
            ['editorial', 'editorial', 'editorial', 'editorial', 'editorial', 
             'hobbies', 'editorial', 'editorial', 'hobbies', 'hobbies', 
             'editorial', 'news', 'news', 'news', 'news'])

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestNounClassification))
    return suite
