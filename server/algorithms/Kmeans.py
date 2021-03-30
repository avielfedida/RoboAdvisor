from app.extensions import db
import pandas as pd
import numpy as np
import scipy.optimize
from algorithms.Algorithm import Algorithm
from sklearn.cluster import KMeans


class Kmeans(Algorithm):

    def __init__(self, risk_score):
        super().__init__(risk_score)
        self.df_cap_bonds_and_stocks = pd.DataFrame(columns=['ticker', 'market_cap'])
        dates = self.prices_df.index
        self.df_prices_bonds_and_stocks = pd.DataFrame(index=dates, columns=self.selected_assets)
        self.set_dfs()
        self.n = len(self.selected_assets)
