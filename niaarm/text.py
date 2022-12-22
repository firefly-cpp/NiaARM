import os
import string
import numpy as np
import pandas as pd
from collections import Counter
from pathlib import Path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from niaarm.rule import Rule
from niaarm.niaarm import NiaARM, _cut_point


def normalize(a, order=2, axis=-1):
    norm = np.atleast_1d(np.linalg.norm(a, order, axis))
    norm[norm == 0] = 1
    return a / np.expand_dims(norm, axis)


class Document:
    """A text document class.

    Args:
        text (str): Document text.
        language (str): Document language. Used for tokenization and stopword removal. Default: 'english'.
        remove_stopwords (bool): If ``True``, remove stopwords from text. Default: ``True``.
        lowercase (bool): If ``True``, make text lowercase. Default: ``True``.

    """

    def __init__(self, text, language='english', remove_stopwords=True, lowercase=True):
        if lowercase:
            text = text.lower()
        self.terms = word_tokenize(text, language)

        self.terms = [term for term in self.terms if term not in string.punctuation]

        if remove_stopwords:
            sw = stopwords.words(language)
            self.terms = [term for term in self.terms if term not in sw]

        self.frequencies = Counter(self.terms)

    def frequency(self, term):
        """Get the frequency of a term,

        Args:
            term (str): Term to get frequency of.

        Returns:
            float: Frequency of the term.

        """
        return self.frequencies[term] / len(self)

    def __getitem__(self, i):
        return self.terms[i]

    def __contains__(self, term):
        return term in self.terms

    def __len__(self):
        return len(self.terms)

    @classmethod
    def from_file(cls, path, encoding='utf-8', language='english', remove_stopwords=True, lowercase=True):
        """Construct document from a plain text file.

        Args:
            path (str): Path to file.
            encoding (str): Encoding of the file. Default: 'utf-8'.
            language (str): Language of the file. Default: 'english'.
            remove_stopwords (bool): If ``True``, remove stopwords from text. Default: ``True``.
            lowercase (bool): If ``True``, make text lowercase. Default: ``True``.

        Returns:
            Document: The constructed document.

        """
        text = Path(path).read_text(encoding)
        return cls(text, language, remove_stopwords, lowercase)


class Corpus:
    """The text corpus class.

    Args:
        documents (Optional[list[Document]]): List of documents. If ``None``, an empty list will be created. Default: ``None``.

    """

    def __init__(self, documents=None):
        self.documents = documents or []

    def append(self, document):
        """Add a document to the corpus.

        Args:
            document (Document): Document to append.

        """
        self.documents.append(document)

    def terms(self):
        """Get a list of unique terms in the corpus

        Returns:
            list[str]: List of unique terms in the corpus.

        """
        all_terms = set()
        for doc in self.documents:
            all_terms.update(doc.terms)
        return sorted(all_terms)

    def __getitem__(self, i):
        return self.documents[i]

    def __len__(self):
        return len(self.documents)

    @classmethod
    def from_list(cls, lst, language='english', remove_stopwords=True, lowercase=True):
        """Construct corpus from a list of strings.

        Args:
            lst (list[str]): List of documents as strings.
            language (str): Language of the file. Default: 'english'.
            remove_stopwords (bool): If ``True``, remove stopwords from text. Default: ``True``.
            lowercase (bool): If ``True``, make text lowercase. Default: ``True``.

        Returns:
            Corpus: The constructed corpus.

        """
        return cls([Document(text, language, remove_stopwords, lowercase) for text in lst])

    @classmethod
    def from_directory(cls, path, encoding='utf-8', language='english', remove_stopwords=True, lowercase=True):
        """Construct corpus from a directory containing plain text files.

        Args:
            path (str): Path to directory.
            encoding (str): Encoding of the files. Default: 'utf-8'.
            language (str): Language of the files. Default: 'english'.
            remove_stopwords (bool): If ``True``, remove stopwords from text. Default: ``True``.
            lowercase (bool): If ``True``, make text lowercase. Default: ``True``.

        Returns:
            Corpus: The constructed corpus.

        """
        documents = []
        for entry in os.scandir(path):
            if entry.is_file():
                documents.append(Document.from_file(entry.path, encoding, language, remove_stopwords, lowercase))
        return cls(documents)

    def tf_idf_matrix(self, smooth=True, norm=2):
        """Get the tf-idf weights matrix as a pandas DataFrame.

        Args:
            smooth (bool): Smooth idf by adding one to the numerator and the denominator to prevent division by 0 errors.
             Default: ``True``.
            norm (int): Order of the norm to normalize the matrix with. Default: 2.

        Returns:
            pd.DataFrame: The tf-idf matrix.

        """
        terms = self.terms()
        num_terms = len(terms)
        num_docs = len(self.documents)
        tf = np.empty((num_docs, num_terms))

        for i, doc in enumerate(self.documents):
            for j, term in enumerate(terms):
                tf[i, j] = doc.frequency(term)

        idf = np.empty(num_terms)
        for i, term in enumerate(terms):
            n = len(self.documents) + smooth
            df = sum(term in doc for doc in self.documents) + smooth
            idf[i] = n / df
        idf = np.log(idf) + 1

        tf_idf = normalize(tf * idf, norm)
        return pd.DataFrame(tf_idf, columns=terms)


class TextRule(Rule):
    r"""Class representing a text association rule.

    The class contains all the metrics in :class:`~niaarm.rule.Rule`, except for amplitude, which returns nan.

    Args:
        antecedent (list[str]): A list of antecedent terms of the text rule.
        consequent (list[str]): A list of consequent terms of the text rule.
        fitness (Optional[float]): Fitness value of the text rule.
        transactions (Optional[pandas.DataFrame]): The tf-idf matrix as a pandas DataFrame.
        threshold (Optional[float]): Threshold of tf-idf weights. If a weight is less than or equal to the
         threshold, the term is not included in the transaction. Default: 0.

    Attributes:
        aws: The sum of tf-idf values for all the terms in the rule.

    See Also:
        :class:`niaarm.rule.Rule`

    """

    __slots__ = (
        'antecedent', 'consequent', 'fitness', 'num_transactions', 'full_count', 'antecedent_count', 'consequent_count',
        'ant_not_con', 'con_not_ant', 'not_ant_not_con', '__inclusion', '__aws'
    )

    metrics = (
        'support', 'confidence', 'lift', 'coverage', 'rhs_support', 'conviction', 'inclusion', 'interestingness',
        'comprehensibility', 'netconf', 'yulesq', 'aws'
    )

    def __init__(self, antecedent, consequent, fitness=0.0, transactions=None, threshold=0):
        super().__init__(antecedent, consequent, fitness, transactions=None)

        if transactions is not None:
            self.num_transactions = len(transactions)
            self.__inclusion = (len(self.antecedent) + len(self.consequent)) / len(transactions.columns)
            self.__post_init__(transactions, threshold)

    def __post_init__(self, transactions, threshold=0):
        self.__inclusion = (len(self.antecedent) + len(self.consequent)) / len(transactions.columns)
        self.__aws = transactions[self.antecedent + self.consequent].values.sum()
        contains_antecedent = (transactions[self.antecedent] > threshold).all(axis=1)
        contains_consequent = (transactions[self.consequent] > threshold).all(axis=1)
        self.antecedent_count = contains_antecedent.sum()
        self.consequent_count = contains_consequent.sum()
        self.full_count = (contains_antecedent & contains_consequent).sum()
        self.ant_not_con = (~contains_consequent & contains_antecedent).sum()
        self.con_not_ant = (contains_consequent & ~contains_antecedent).sum()
        self.not_ant_not_con = (~contains_antecedent & ~contains_consequent).sum()

    @property
    def amplitude(self):
        return np.nan

    @property
    def inclusion(self):
        return self.__inclusion

    @property
    def aws(self):
        return self.__aws


class NiaARTM(NiaARM):
    r"""Representation of Association Rule Text Mining as an optimization problem.

    The implementation is composed of ideas found in the following paper:

    * I. Fister, S. Deb, I. Fister, „Population-based metaheuristics for Association Rule Text Mining“,
      in Proceedings of the 2020 4th International Conference on Intelligent Systems, Metaheuristics & Swarm Intelligence,
      New York, NY, USA, mar. 2020, pp. 19–23. doi: 10.1145/3396474.3396493.

    Args:
        max_terms (int): Maximum number of terms in association rule..
        features (list[str]): List of unique terms in the corpus.
        transactions (pandas.Dataframe): The tf-idf matrix.
        metrics (Union[Dict[str, float], Sequence[str]]): Metrics to take into account when computing the fitness.
         Metrics can either be passed as a Dict of pairs {'metric_name': <weight of metric>} or
         a sequence of metrics as strings, in which case, the weights of the metrics will be set to 1.
        threshold (Optional[float]): Threshold of tf-idf weights. If a weight is less than or equal to the
         threshold, the term is not included in the transaction. Default: 0.
        logging (bool): Enable logging of fitness improvements. Default: ``False``.

    Attributes:
        rules (RuleList): A list of mined text rules.

    """

    available_metrics = (
        'support', 'confidence', 'coverage', 'interestingness', 'comprehensibility', 'inclusion', 'rhs_support', 'aws'
    )

    def __init__(self, max_terms, terms, transactions, metrics, threshold=0, logging=False):
        super().__init__(max_terms + 1, terms, transactions, metrics, logging)
        self.max_terms = max_terms
        self.threshold = threshold

    def build_rule(self, vector):
        terms = [self.features[int(val * (self.num_features - 1))] for val in vector]

        seen = set()
        rule = []
        for term in terms:
            if term in seen:
                continue
            rule.append(term)
            seen.add(term)

        return rule

    def _evaluate(self, x):
        cut_value = x[self.dimension - 1]
        solution = x[:-1]

        rule = self.build_rule(solution)
        cut = _cut_point(cut_value, len(rule))

        antecedent = rule[:cut]
        consequent = rule[cut:]

        if antecedent and consequent:
            rule = TextRule(antecedent, consequent, transactions=self.transactions, threshold=self.threshold)
            metrics = [getattr(rule, metric) for metric in self.metrics]
            fitness = np.dot(self.weights, metrics) / self.sum_weights
            rule.fitness = fitness

            if rule.support > 0.0 and rule.confidence > 0.0 and rule not in self.rules:
                self.rules.append(rule)

                if self.logging and fitness > self.best_fitness:
                    self.best_fitness = fitness
                    print(f'Fitness: {rule.fitness}, ' + ', '.join(
                        [f'{metric.capitalize()}: {metrics[i]}' for i, metric in enumerate(self.metrics)]))
            return fitness
        else:
            return -1.0
