from collections import OrderedDict
import numpy as np
import spacy
import inflect
import nltk

nlp = spacy.load("en_core_web_sm")
plu = inflect.engine()

class TextRank4Keyword():
    """Extract keywords from text"""

    def __init__(self):
        self.d = 0.85 # damping coefficient, usually is .85
        self.min_diff = 1e-5 # convergence threshold
        self.steps = 20 # iteration steps
        self.node_weight = None # save keywords and its weight

    def sentence_segment(self, str, candidate_pos):
        """Store those words only in candidate_pos"""
        tokens = nltk.word_tokenize(str)

        keywordSent = []
        pos = nltk.pos_tag(tokens)
        i = 0
        print(len(pos))
        while (i < len(pos)):
            sent = ""
            # print(i)
            # print(pos[i][0], pos[i][1], i)
            while (pos[i][1] in candidate_pos):
                sent += f"{pos[i][0]} "
                i += 1
            print(sent)

            if pos[i][1] not in candidate_pos:
                i += 1
            if sent != "":
                keywordSent.append(sent.strip())


        print(keywordSent)

        res1 = []

        for i in keywordSent:
            if i not in res1:
                res1.append(i)

        out = map(lambda x:x.lower(), res1)
        res2 = list(out)

        res3 = []

        for i in res2:
            if i in res3:
                res3.append(False)
            else:
                res3.append(i)

        i = 0
        while (i < len(res3)):
            if res3[i] == False:
                res3.pop(i)
                res1.pop(i)
            i += 1

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

    def symmetrize(self, g):
        return g + g.T - np.diag(g.diagonal())

    def get_matrix(self, vocab, token_pairs):
        """Get normalized matrix"""

        # Build matrix
        vocab_size = len(vocab)
        g = np.zeros((vocab_size, vocab_size), dtype='float')
        for word_1, word_2 in token_pairs:
            i, j = vocab[word_1], vocab[word_2]
            g[i][j] = 1

        # Get Symmeric matrix
        g = self.symmetrize(g)

        # Normalize matrix by column
        normal = np.sum(g, axis=0)
        g_norm = np.divide(g, normal, where=normal!=0) # ignore the 0 element in normal

        return g_norm


    def get_keywords(self, number):
        """Print top number keywords"""
        keywords = list()
        node_weight = OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))
        for i, (key, value) in enumerate(node_weight.items()):
            print(key + ' - ' + str(value))
            keywords.append(key)
            if i >= number:
                break
        print("\n\n")
        print(set(keywords))


    def analyze(self, text, candidate_pos, window_size=4):
        """Main function to analyze text"""

        # Filter sentences
        sentences = self.sentence_segment(text, candidate_pos)

        # Build vocabulary
        vocab = self.get_vocab(sentences)

        # Get token_pairs from windows
        token_pairs = self.get_token_pairs(window_size, sentences)

        # Get normalized matrix
        g = self.get_matrix(vocab, token_pairs)

        # Initialization for weight (PageRank value)
        pr = np.array([1] * len(vocab))

        # Iteration for weight
        previous_pr = 0
        for epoch in range(self.steps):
            pr = (1 - self.d) + self.d * np.dot(g, pr)
            if abs(previous_pr - sum(pr))  < self.min_diff:
                break
            else:
                previous_pr = sum(pr)

        # Get weight for each node
        node_weight = dict()
        for word, index in vocab.items():
            node_weight[word] = pr[index]

        self.node_weight = node_weight


if __name__ == "__main__":
    content = '''
    Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types systems and systems of mixed types.
    '''

    text = '''
    The Wandering Earth, described as Chinas first big-budget science fiction thriller, quietly made it onto screens at AMC theaters in North America this weekend, and it shows a new side of Chinese filmmaking — one focused toward futuristic spectacles rather than Chinas traditionally grand, massive historical epics. At the same time, The Wandering Earth feels like a throwback to a few familiar eras of American filmmaking. While the films cast, setting, and tone are all Chinese, longtime science
    '''

    textrank = TextRank4Keyword()
    textrank.analyze(text, candidate_pos = ['NN', 'NNS', 'JJ', 'NNP'])
    textrank.get_keywords(10)
