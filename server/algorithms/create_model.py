from algorithms.black_litterman import BlackLitterman
from algorithms.markowitz import Markowitz

def create_model(model_name, risk):
    if model_name == 'markowitz':
        return Markowitz(risk)
    if model_name == 'blackLitterman':
        return BlackLitterman(risk)

    # todo add more models
