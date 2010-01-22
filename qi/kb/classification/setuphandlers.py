from nltk.downloader import download
import logging

def downloadNLTKData(context):
    """
    """
    logger = logging.getLogger('qi.kb.classification')    
    logger.info("Downloading NLTK's Punkt Tokenizer Models")
    download('punkt')
    logger.info("Downloading NLTK's Brown corpus")
    download('brown')
    logger.info("Downloading NLTK's Treebank POS Tagger (Max entropy)")
    download('maxent_treebank_pos_tagger')
        