from collections import OrderedDict
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import inflect

nlp = spacy.load("en_core_web_sm")
plu = inflect.engine()

class TextRankKeyword():
    """Extract keywords from text"""

    def __init__(self):
        self.d = 0.85 # damping coefficient, usually is .85
        self.min_dif = 1e-5 # convergence threshold
        self.step = 20 # iteration steps
        self.nodes_weight = None # save keywords and its weight

    def _stopwords(self):
        """Set stop words"""
        for word in STOP_WORDS:
            lexeme = nlp.vocab[word]
            lexeme.is_stop = True

    def sentence_segment(self, doc, candidate_pos):
        """Store those words only in candidate_pos"""

        keywordSent = []

        # Segment sentences according to stopwords and candidate_pos
        for sent in doc.sents:
            i = 0
            while (True):
                sents = ""
                while (sent[i].pos_ in candidate_pos and sent[i].is_stop is False):
                    sents += f'{sent[i].text} '
                    i += 1

                if sent[i].pos_ not in candidate_pos or sent[i].is_stop is True:
                    i += 1

                if sents != "":
                    keywordSent.append(sents.strip())

                if i >= len(sent):
                    break

        # Remove the redundant words by checking uppercase and lowercase
        res1 = []

        for i in keywordSent:
            if i not in res1:
                res1.append(i)


        out = map(lambda x:x.lower(), res1)
        res2 = list(out)

        i = 0
        while i < len(res1):
            j = i + 1
            l = len(res1)
            while j < l:
                if res1[i].lower() in res2[j:] and res1[j].islower() is False:
                    indx = res2[j:].index(res1[i].lower())
                    res1.pop(j + indx)
                    res2.pop(j + indx)
                    l -= 1
                j +=1
            i += 1

        # Remove redundant words by checking singular and plural
        res2 = []

        l = len(res1)
        singFlag = 0

        i = 0
        while (i < l):
            j = i + 1
            while (j < l):
                if plu.singular_noun(res1[j]) == res1[i]:
                    res2.append(res1[j])
                    res1.pop(i)
                    l -= 1
                    break
                elif res1[j] == plu.singular_noun(res1[i]):
                    res2.append(res1[i])
                    res1.pop(j)
                    l -= 1
                    break
                else:
                    singFlag = 1

                j += 1

            if singFlag == 1:
                if res1[i] not in res2:
                    res2.append(res1[i])

            i += 1
        return res2

    def get_vocab(self, sentences):
        """Get all tokens"""
        vocab = OrderedDict()
        i = 0
        for word in sentences:
            if word not in vocab:
                vocab[word] = i
                i += 1
        return vocab

    def get_token_pairs(self, window_size, sentences):
        """Build token_pairs from windows in sentences"""
        token_pairs = list()
        for i, word in enumerate(sentences):
            for j in range(i+1, i+window_size):
                if j >= len(sentences):
                    break
                pair = (word, sentences[j])
                if pair not in token_pairs:
                    token_pairs.append(pair)
        return token_pairs

    def symmetricize(self, mat):
        return mat + mat.T - np.diag(mat.diagonal())

    def get_matrix(self, vocab, token_pairs):
        """Get normalized matrix"""

        # Build matrix
        vocab_size = len(vocab)
        mat = np.zeros((vocab_size, vocab_size), dtype='float')
        for word_1, word_2 in token_pairs:
            i, j = vocab[word_1], vocab[word_2]
            mat[i][j] = 1

        # Get Symmetric matrix
        mat = self.symmetricize(mat)

        # Normalize matrix by column
        normal = np.sum(mat, axis=0)
        mat_norm = np.divide(mat, normal, where=normal!=0) # ignore the 0 element in normal

        return mat_norm


    def get_keywords(self, number):
        """Print top number keywords"""
        keywords = set()
        nodes_weight = OrderedDict(sorted(self.nodes_weight.items(), key=lambda t: t[1], reverse=True))
        for index, (key, value) in enumerate(nodes_weight.items()):
            print(key + ' - ' + str(value))
            keywords.add(key)
            if index >= number:
                break
        print(f'\n{keywords}')


    def analyze(self, text, candidate_pos, window_size=4):
        """Main function to analyze text"""

        # Set stop words
        self._stopwords()

        # Parse input text
        doc = nlp(text)

        # Filter sentences
        sentences = self.sentence_segment(doc, candidate_pos)

        # Build vocab
        vocab = self.get_vocab(sentences)

        # Get token_pairs from windows
        token_pairs = self.get_token_pairs(window_size, sentences)

        # Get normalized matrix
        mat = self.get_matrix(vocab, token_pairs)

        # Initialization for weight (PageRank value)
        pageR = np.array([1] * len(vocab))

        # Iteration for weight
        previous_pageR = 0
        for epoch in range(self.step):
            pageR = (1 - self.d) + self.d * np.dot(mat, pageR)
            if abs(previous_pageR - sum(pageR))  < self.min_dif:
                break
            else:
                previous_pageR = sum(pageR)

        # Get weights for each node
        nodes_weight = dict()
        for word, index in vocab.items():
            nodes_weight[word] = pageR[index]

        self.nodes_weight = nodes_weight


if __name__ == "__main__":

    text = '''
    The Wandering Earth, described as Chinas first big-budget science fiction thriller, quietly made it onto screens at AMC theaters in North America this weekend, and it shows a new side of Chinese filmmaking — one focused toward futuristic spectacles rather than China’s traditionally grand, massive historical epics. At the same time, The Wandering Earth feels like a throwback to a few familiar eras of American filmmaking. While the film’s cast, setting, and tone are all Chinese, longtime science
    '''

    textrank = TextRankKeyword()

    # NOUN and PROPER NOUN (PROPN) only selected while segmenting sentences
    textrank.analyze(text, candidate_pos = ['NOUN', 'PROPN'])

    textrank.get_keywords(10)
