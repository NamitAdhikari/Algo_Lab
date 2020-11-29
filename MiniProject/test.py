import spacy
# from textrank_final2 import TextRankKeyword

nlp = spacy.load("en_core_web_sm")

content = '''
Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types systems and systems of mixed types.
'''

doc = nlp(content)
candidate_pos = ['NOUN', 'PROPN']

# textrank = TextRankKeyword()
sentlist = []

for sent in doc.sents:
    for st in sent.noun_chunks:
        print(st, len(st))
        if len(st) == 1:
            sentlist.append(f'{st.text}')
        elif len(st) > 1:
            i = 0
            while (True):
                sent1 = ""
                while (st[i].pos_ in candidate_pos and st[i].is_stop is False):
                    sent1 += f'{st[i].text} '
                    i += 1

                if st[i].pos_ not in candidate_pos or st[i].is_stop:
                    i += 1

                if sent1 != "":
                    sentlist.append(sent1.strip())

                if i >= len(st):
                    break

print(sentlist)
