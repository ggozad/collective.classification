from zope.interface import implements
from nltk import pos_tag
from nltk.tag import AffixTagger, UnigramTagger, BigramTagger, \
    TrigramTagger, DefaultTagger, brill
from collective.classification.interfaces import IPOSTagger

class PennTreebankTagger(object):
    """Tokenizes text using the default nltk tagger, based on Penn Treebank
    """

    implements(IPOSTagger)

    def train(self,sentence_list):
        pass

    def tag(self,words):
        """
        """
        return pos_tag(words)

class TriGramTagger(object):
    """ Trigram tagger
    """

    implements(IPOSTagger)

    def __init__(self):
        self.tagger = None

    def train(self,sentence_list):
        """
        """
        noun_fallback = DefaultTagger('NN')
        affix_fallback = AffixTagger(sentence_list,
            backoff=noun_fallback)
        unigram_fallback = UnigramTagger(sentence_list,
            backoff=affix_fallback)
        bigram_fallback = BigramTagger(sentence_list,
            backoff=unigram_fallback)
        self.tagger = TrigramTagger(sentence_list,
            backoff=bigram_fallback)

    def tag(self,words):
        """
        """
        if not self.tagger:
            raise Exception("Trigram Tagger not trained.")
        return self.tagger.tag(words)

class BrillTrigramTagger(object):
    """
    """

    implements(IPOSTagger)

    def __init__(self):
        self.tagger = None

    def train(self,sentence_list):
        """Trains the tagger from the tagged sentences provided
        """
        noun_fallback = DefaultTagger('NN')
        affix_fallback = AffixTagger(sentence_list,
            backoff=noun_fallback)
        unigram_fallback = UnigramTagger(sentence_list,
            backoff=affix_fallback)
        bigram_fallback = BigramTagger(sentence_list,
            backoff=unigram_fallback)
        trigram_fallback = TrigramTagger(sentence_list,
            backoff=bigram_fallback)
        templates = [
            brill.SymmetricProximateTokensTemplate(
                brill.ProximateTagsRule, (1,1)),
            brill.SymmetricProximateTokensTemplate(
                brill.ProximateTagsRule, (2,2)),
            brill.SymmetricProximateTokensTemplate(
                brill.ProximateTagsRule, (1,2)),
            brill.SymmetricProximateTokensTemplate(
                brill.ProximateTagsRule, (1,3)),
            brill.SymmetricProximateTokensTemplate(
                brill.ProximateWordsRule, (1,1)),
            brill.SymmetricProximateTokensTemplate(
                brill.ProximateWordsRule, (2,2)),
            brill.SymmetricProximateTokensTemplate(
                brill.ProximateWordsRule, (1,2)),
            brill.SymmetricProximateTokensTemplate(
                brill.ProximateWordsRule, (1,3)),
            brill.ProximateTokensTemplate(
                brill.ProximateTagsRule, (-1, -1), (1,1)),
            brill.ProximateTokensTemplate(
                brill.ProximateWordsRule, (-1, -1), (1,1))
        ]
        trainer = brill.FastBrillTaggerTrainer(trigram_fallback, templates)
        self.tagger = trainer.train(sentence_list,max_rules=100,min_score=3)

    def tag(self,words):
        """
        """
        if not self.tagger:
            raise Exception("Brill Tagger not trained.")
        return self.tagger.tag(words)
