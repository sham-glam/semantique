#

import banglanltk as bn

# For single word
print(bn.stemmer('শান্তিনিকেতনে'))

# For multiple words
text = 'আজ বৃষ্টি হবে।'
words = bn.word_tokenize(text)
for w in words:
    print(bn.stemmer(w))

    