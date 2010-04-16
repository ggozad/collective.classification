import logging
from nltk.downloader import download

def downloadNLTKTokenizerData():
    logger = logging.getLogger('collective.classification')
    logger.info("Downloading NLTK's Punkt Tokenizer Models")
    download('punkt')

def downloadNLTKBrownCorpus():
    logger = logging.getLogger('collective.classification')
    logger.info("Downloading NLTK's Brown corpus")
    download('brown')

def downloadNLTKPenTreeBank():
    logger = logging.getLogger('collective.classification')
    logger.info("Downloading NLTK's Treebank POS Tagger (Max entropy)")
    download('maxent_treebank_pos_tagger')