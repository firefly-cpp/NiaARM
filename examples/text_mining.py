import pandas as pd
from niaarm.text import Corpus
from niaarm.mine import get_text_rules
from niapy.algorithms.basic import ParticleSwarmOptimization

# load corpus and extract the documents as a list of strings
df = pd.read_json("datasets/text/artm_test_dataset.json", orient="records")
documents = df["text"].tolist()

# create a Corpus object from the documents (requires nltk's punkt_tab tokenizer and the stopwords list)
try:
    corpus = Corpus.from_list(documents)
except LookupError:
    import nltk

    nltk.download("punkt_tab")
    nltk.download("stopwords")
    corpus = Corpus.from_list(documents)

# the rest is pretty much the same as with the numerical association rules
# 1. Init algorithm
# 2. Define metrics
# 3. Run algorithm
algorithm = ParticleSwarmOptimization(population_size=200, seed=123)
metrics = ("support", "confidence", "aws")
rules, time = get_text_rules(
    corpus,
    max_terms=8,
    algorithm=algorithm,
    metrics=metrics,
    max_evals=10000,
    logging=True,
)

print(rules)
print(f"Run time: {time:.2f}s")
rules.to_csv("output.csv")
