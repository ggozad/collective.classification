import nltk


class Tokenizer(object):

    def tokenize(self, text):
        sentences = self.sent_tokenizer.tokenize(text)
        tokens = []
        for sentence in sentences:
            tokens = tokens + nltk.word_tokenize(sentence)
        return tokens
