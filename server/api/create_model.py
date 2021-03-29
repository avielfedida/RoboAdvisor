from api.black_litterman import BlackLitterman
from api.Algorithm import Markowitz

def create_model(model_name, risk):
    if model_name == 'markowitz':
        return Markowitz(risk)
    if model_name == 'black_litterman':
        return BlackLitterman(model_name, risk)

    # todo add more models
