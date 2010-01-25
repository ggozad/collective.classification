from qi.kb.classification.tests.base import ClassificationFunctionalTestCase
from zope.component import getUtility
from qi.kb.classification.interfaces import IContentClassifier
from nltk.corpus import brown

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
    
    def test_tags(self):    
        self.login()
        news_ids = [
            (fileid,'news') 
            for fileid in brown.fileids(categories='news')[:6]]
                    
        editorial_ids = [
            (fileid,'editorial') 
            for fileid in brown.fileids(categories='editorial')[:6]]
        
        for (articleid,subject) in news_ids[:5]+editorial_ids[:5]:
            text = " ".join(brown.words(articleid))
            self.folder.invokeFactory('Document',articleid,
                                      text=text,
                                      subject=subject)
        self.assertEquals(self.classifier.tags(),['editorial','news'])
        
        for (articleid,subject) in news_ids[5:6]+editorial_ids[5:6]:
            text = " ".join(brown.words(articleid))
            self.folder.invokeFactory('Document',articleid,text=text)

        #items already classified should always suggest their own subjects
        browser = self.getBrowser()
        browser.open(self.folder.absolute_url()+'/ca01/@@subjectsuggest')
        self.failUnless("news 100.0%" in browser.contents)
        self.failUnless("editorial 0.0%" in browser.contents)
        
        #a test item belogining to the 'news' category
        browser.open(self.folder.absolute_url()+'/ca06/@@subjectsuggest')
        self.failUnless("news 70.0%" in browser.contents)

        #a test item belogining to the 'editorial' category
        browser.open(self.folder.absolute_url()+'/cb06/@@subjectsuggest')
        self.failUnless("editorial 96.5%" in browser.contents)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestIntegration))
    return suite
