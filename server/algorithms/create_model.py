from algorithms.black_litterman import BlackLitterman
from algorithms.markowitz import Markowitz
from algorithms.Kmeans import Kmeans
from algorithms.mean_gini import Gini


def create_model(model_name, risk):
    if model_name == 'markowitz':
        return Markowitz(risk, model_name)
    if model_name == 'blackLitterman':
        return BlackLitterman(risk, model_name)
    if model_name == 'mean_gini':
        return Gini(risk, model_name)
    if model_name == 'Kmeans':
        return Kmeans(risk, model_name)

