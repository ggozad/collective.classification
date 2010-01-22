from qi.kb.classification.tests.base import ClassificationFunctionalTestCase
from qi.kb.classification.tests.util import readData
from zope.component import getUtility
from qi.kb.classification.interfaces import IContentClassifier
from qi.kb.classification.interfaces import IPOSTagger
from nltk.corpus import brown
from qi.kb.classification.classifiers.npextractor import NPExtractor
from Products.Five.testbrowser import Browser

class TestIntegration(ClassificationFunctionalTestCase):
    """Plone integration tests. Test the Naive Bayes document classifier using 
    only the most frequent nouns as input. As sample test we train the 
    classifier with a few articles from the Brown corpus categorised as
    'editorial'  and a few others categorised as 'hobbies'. Then, we test the 
    classifier with 15 additional documents, getting 12/15 right.
    """
    
    def afterSetUp(self):
        """
        """
        self.classifier = getUtility(IContentClassifier)
        #tagged_sents =  brown.tagged_sents(
        #    categories=['hobbies','news'])
        #tagger = getUtility(IPOSTagger,
        #    name="qi.kb.termextraxt.taggers.NgramTagger")
        #tagger.train(tagged_sents)
        #extractor = NPExtractor(tagger=tagger)
        #self.classifier.extractor = extractor
    
    def test_tags(self):    
        self.login()
        
        news_ids = [("ca%.2i.txt"%i,'news',) for i in range(1,7)]
        editorial_ids = [("cb%.2i.txt"%i,'editorial',) for i in range(1,7)]
        
        for (articleid,subject) in news_ids[:5]+editorial_ids[:5]:
            text = readData(articleid)
            self.folder.invokeFactory('Document',articleid,
                                      text=text,
                                      subject=subject)
        self.assertEquals(self.classifier.tags(),['editorial','news'])
        
        for (articleid,subject) in news_ids[5:6]+editorial_ids[5:6]:
            text = readData(articleid)
            self.folder.invokeFactory('Document',articleid,text=text)

        #items already classified should always suggest their own subjects
        browser = self.getBrowser()
        browser.open(self.folder.absolute_url()+'/ca01.txt/@@subjectsuggest')
        self.failUnless("news 100.0%" in browser.contents)
        self.failUnless("editorial 0.0%" in browser.contents)
        
        browser.open(self.folder.absolute_url()+'/ca06.txt/@@subjectsuggest')
        self.failUnless("news 70.0%" in browser.contents)

        browser.open(self.folder.absolute_url()+'/cb06.txt/@@subjectsuggest')
        self.failUnless("editorial 96.5%" in browser.contents)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestIntegration))
    return suite
