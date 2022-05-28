import pandas as pd
from niaarm.text import Corpus
from niaarm.mine import get_text_rules
from niapy.algorithms.basic import ParticleSwarmOptimization

df = pd.read_json('datasets/text/artm_test_dataset.json', orient='records')
documents = df['text'].tolist()
corpus = Corpus.from_list(documents)

algorithm = ParticleSwarmOptimization(population_size=200, seed=123)
metrics = ('support', 'confidence', 'aws')
rules, time = get_text_rules(corpus, max_terms=5, algorithm=algorithm, metrics=metrics, max_evals=10000, logging=True)

if len(rules):
    print(rules)
    print(f'Run time: {time:.2f}s')
    rules.to_csv('output.csv')
else:
    print('No rules generated')
    print(f'Run time: {time:.2f}s')
