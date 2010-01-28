from zope.i18nmessageid import MessageFactory
from qi.kb.classification.nltkutilities.downloader import downloadNLTKData
ClassificationMessageFactory = MessageFactory('qi.kb.classification')
downloadNLTKData()

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
