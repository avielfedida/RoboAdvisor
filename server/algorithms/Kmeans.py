from app.extensions import db
import pandas as pd
import numpy as np
from algorithms.Algorithm import Algorithm
from sklearn.cluster import KMeans
import scipy.optimize as optimizer
from kneed import KneeLocator
from scipy.cluster.vq import kmeans,vq


class Kmeans(Algorithm):

    def __init__(self, risk_score, model_name):
        super().__init__(risk_score, model_name)
        prices_df = self.get_assets_price_data_from_db()
        dates = self.prices_df.index
        self.df_prices_bonds_and_stocks = pd.DataFrame(index=dates, columns=self.selected_assets)

    def get_optimal_portfolio(self):
        sharpe_portfolio = pd.DataFrame(columns=['Ticker', 'Weight'])
        weights = 100 / self.k_means()
        for i in range(len(self.selected_assets)):
            ticker = self.selected_assets[i]
            weight = weights[i]
            sharpe_portfolio = sharpe_portfolio.append({'Ticker': ticker, 'Weight': weight}, ignore_index=True)
        sharpe_portfolio = sharpe_portfolio.set_index('Ticker')
        return sharpe_portfolio

    def k_means(self):
        returns = self.prices_df.pct_change().mean() * 252
        returns = pd.DataFrame(returns)
        returns.columns = ['Returns']
        returns['Volatility'] = self.prices_df.pct_change().std() * np.sqrt(252)
        data = np.asarray([np.asarray(returns['Returns']), np.asarray(returns['Volatility'])]).T
        X = data
        distorsions = []
        for k in range(2, 50):
            k_means = KMeans(n_clusters=k)
            k_means.fit(X)
            distorsions.append(k_means.inertia_)
        y = distorsions
        x = range(1, len(y) + 1)
        kn = KneeLocator(x, y, curve='convex', direction='decreasing')
        k = kn.knee
        centroids, _ = kmeans(data, k)
        # assign each sample to a cluster
        idx, _ = vq(data, centroids)
        # drop the relevant stock from our data
        returns.drop(returns.idxmax(), inplace=True)
        # recreate data to feed into the algorithm
        data = np.asarray([np.asarray(returns['Returns']), np.asarray(returns['Volatility'])]).T
        centroids, _ = kmeans(data, k)
        # assign each sample to a cluster
        idx, _ = vq(data, centroids)
        details = [(name, cluster) for name, cluster in zip(returns.index, idx)]
        details_df = pd.DataFrame(details)
        details_df.columns = ['name', 'cluster']
        df_clusters_and_returns = pd.merge(details_df, returns, left_on='name', right_on=returns.index, how='inner')
        return k

