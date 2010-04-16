from zope.i18nmessageid import MessageFactory
from collective.classification.data.downloader import downloadNLTKTokenizerData
ClassificationMessageFactory = MessageFactory('collective.classification')
downloadNLTKTokenizerData()

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
