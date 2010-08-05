from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase.layer import PloneSite
from collective.classification.data import downloader


class ClassificationLayer(PloneSite):

    @classmethod
    def setUp(cls):
        fiveconfigure.debug_mode = True
        import collective.classification
        zcml.load_config('configure.zcml', collective.classification)
        fiveconfigure.debug_mode = False
        downloader.downloadNLTKPenTreeBank()
        downloader.downloadNLTKBrownCorpus()

    @classmethod
    def tearDown(cls):
        pass
