import pickle
from nltk.tag import AffixTagger, UnigramTagger, BigramTagger, \
    TrigramTagger, DefaultTagger, brill

class TriGramTrainer(object):
    """ Trigram tagger trainer
    """

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
        self.tagger = TrigramTagger(sentence_list,
            backoff=bigram_fallback)

    def dump(self,filename='trigram.pickle'):
        try:
            file = open(filename,"w")
            pickle.dump(self.tagger,file)
        finally:
            file.close()

class BrillTrainer(object):
    """
    """

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
            brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,1)),
            brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (2,2)),
            brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,2)),
            brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,3)),
            brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,1)),
            brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (2,2)),
            brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,2)),
            brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,3)),
            brill.ProximateTokensTemplate(brill.ProximateTagsRule, (-1, -1), (1,1)),
            brill.ProximateTokensTemplate(brill.ProximateWordsRule, (-1, -1), (1,1))
        ]
        trainer = brill.FastBrillTaggerTrainer(trigram_fallback, templates)
        self.tagger = trainer.train(sentence_list,max_rules=100,min_score=3)

    def dump(self,filename='trigram.pickle'):
        try:
            file = open(filename,"w")
            pickle.dump(self.tagger,file)
        finally:
            file.close()

def english():
    """
    """
    from nltk.corpus import conll2000
    conll2000_sents = conll2000.tagged_sents()
    trainer = BrillTrainer()
    trainer.train(conll2000_sents)
    trainer.dump("english_tagger.pickle")