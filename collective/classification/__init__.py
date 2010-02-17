from zope.i18nmessageid import MessageFactory
from collective.classification.nltkutilities.downloader import downloadNLTKData
ClassificationMessageFactory = MessageFactory('collective.classification')
downloadNLTKData()

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
