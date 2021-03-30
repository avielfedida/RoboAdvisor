from algorithms.black_litterman import BlackLitterman
from algorithms.markowitz import Markowitz

def create_model(model_name, risk):
    if model_name == 'markowitz':
        return Markowitz(risk)
    if model_name == 'black_litterman':
        return BlackLitterman(risk)

    # todo add more models
