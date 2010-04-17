from transaction import commit
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing.ZopeTestCase import app, close, installPackage
from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase.layer import PloneSite
from collective.classification.data import downloader 

class ClassificationLayer(PloneSite):
    @classmethod
    def setUp(cls):
        fiveconfigure.debug_mode = True
        import collective.classification
        zcml.load_config('configure.zcml', collective.classification)
        fiveconfigure.debug_mode = False    
        installPackage('collective.classification',quiet=True)
        # import the default profile
        root = app()
        portal = root.plone
        tool = getToolByName(portal, 'portal_setup')
        profile = 'profile-collective.classification:default'
        tool.runAllImportStepsFromProfile(profile, purge_old=False)
        # and commit the changes
        commit()
        close(root)
        downloader.downloadNLTKPenTreeBank()
        downloader.downloadNLTKBrownCorpus()

    @classmethod
    def tearDown(cls):
        pass
