import os
import string
import numpy as np
import pandas as pd
from collections import Counter
from pathlib import Path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class Document:
    def __init__(self, text, language='english', remove_stopwords=True, lowercase=True):
        if lowercase:
            text = text.lower()
        self.terms = word_tokenize(text, language)

        self.terms = [term for term in self.terms if term not in string.punctuation]

        if remove_stopwords:
            sw = stopwords.words(language)
            self.terms = [term for term in self.terms if term not in sw]

        self.frequencies = Counter(self.terms)

    def unique(self):
        return len(self.frequencies)

    def frequency(self, term):
        return self.frequencies[term] / len(self)

    def __getitem__(self, i):
        return self.terms[i]

    def __contains__(self, term):
        return term in self.terms

    def __len__(self):
        return len(self.terms)

    @classmethod
    def from_file(cls, path, encoding='utf-8', language='english', remove_stopwords=True, lowercase=True):
        text = Path(path).read_text(encoding)
        return cls(text, language, remove_stopwords, lowercase)


class Corpus:
    def __init__(self, documents=None):
        self.documents = documents or []

    def append(self, document):
        self.documents.append(document)

    def terms(self):
        all_terms = set(self.documents[0].terms)
        for doc in self.documents[1:]:
            all_terms.update(doc.terms)
        return sorted(all_terms)

    def __getitem__(self, i):
        return self.documents[i]

    def __len__(self):
        return len(self.documents)

    @classmethod
    def from_list(cls, lst, language='english', remove_stopwords=True, lowercase=True):
        return cls([Document(text, language, remove_stopwords, lowercase) for text in lst])

    @classmethod
    def from_directory(cls, path, encoding='utf-8', language='english', remove_stopwords=True, lowercase=True):
        documents = []
        for entry in os.scandir(path):
            if entry.is_file():
                documents.append(Document.from_file(entry.path, encoding, language, remove_stopwords, lowercase))
        return cls(documents)


def tf_idf(corpus):
    terms = corpus.terms()
    num_terms = len(terms)
    num_docs = len(corpus)
    tf = np.zeros((num_docs, num_terms))

    for i, doc in enumerate(corpus):
        for j, term in enumerate(terms):
            tf[i, j] = doc.frequency(term)

    idf = []
    for term in terms:
        idf.append(len(corpus) / sum(term in doc for doc in corpus))
    idf = np.abs(np.log(idf))

    return tf * idf
