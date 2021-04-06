from app.extensions import db
import pandas as pd
import numpy as np
from algorithms.Algorithm import Algorithm
from sklearn.cluster import KMeans
import scipy.optimize as optimizer
from kneed import KneeLocator
from scipy.cluster.vq import kmeans, vq
import math

class Kmeans(Algorithm):

    def __init__(self, risk_score, model_name):
        super().__init__(risk_score, model_name)
        self.assets = self.get_selected_assets(risk_score)
        self.df_prices_bonds_and_stocks = pd.DataFrame(index=self.prices_df.index, columns=self.selected_assets)
        self.create_df()

    def get_optimal_portfolio(self):
        sharpe_portfolio = pd.DataFrame(columns=['Ticker', 'Weight'])
        k, df_sharpe_ratio_cluster = self.k_means()
        weights = (len(self.df_sharpe_ratio_cluster)) / k
        df = self.choose_stocks(k,self.risk_score, df_sharpe_ratio_cluster)
        for i in range(df):
            ticker = df[i]
            weight = weights[i]
            sharpe_portfolio = sharpe_portfolio.append({'Ticker': ticker, 'Weight': weight}, ignore_index=True)
        sharpe_portfolio = sharpe_portfolio.set_index('Ticker')
        return sharpe_portfolio

    def k_means(self):
        new_prices_df = self.df_prices_bonds_and_stocks
        returns = new_prices_df.pct_change().mean() * 252
        returns = pd.DataFrame(returns)
        returns.columns = ['Returns']
        returns['Volatility'] = new_prices_df.pct_change().std() * np.sqrt(252)
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
        return k, df_clusters_and_returns

    def get_selected_assets(self, risk_score):
        all_std = [self.prices_df[col].std() for col in self.prices_df.columns]
        all_ret = [
            self.prices_df.loc[self.prices_df.index.max(), col] - self.prices_df.loc[self.prices_df.index.min(), col]
            for col in self.prices_df.columns]
        all_sharpe_ratio = self.sharpe_ratio(all_ret, min(all_ret))
        std_df = pd.DataFrame(index=self.prices_df.columns, columns=['std', 'sharpe_ratio'])
        for index, asset in enumerate(self.prices_df.columns):
            std_df.loc[asset, 'std'] = all_std[index]
            std_df.loc[asset, 'sharpe_ratio'] = all_sharpe_ratio[index]
        std_df.sort_values(by=['std', 'sharpe_ratio'], inplace=True)
        take_top = 100
        # return the relevant assets according to the risk level
        size = int(len(std_df) / 5)
        if risk_score == 1:
            selected_assets = std_df.iloc[0:size].index.tolist()[:take_top]
        elif risk_score == 2:
            selected_assets = std_df.iloc[size:size * 2].index.tolist()[:take_top]
        elif risk_score == 3:
            selected_assets = std_df.iloc[size * 2:size * 3].index.tolist()[:take_top]
        elif risk_score == 4:
            selected_assets = std_df.iloc[size * 3:size * 4].index.tolist()[:take_top]
        elif risk_score == 5:
            selected_assets = std_df.iloc[size * 4:size * 5].index.tolist()[:take_top]
        else:
            selected_assets = std_df.index.tolist()[:take_top]
        return selected_assets

    def create_df(self):
        data = pd.read_sql_table('stocks_prices', db.engine)
        for ticker in self.selected_assets:
            self.df_prices_bonds_and_stocks[ticker] = data[data['ticker'] == ticker]['price'].values

    def choose_stocks(self, k, risk, df_sharpe_ratio_cluster):
        size = 20
        amount = math.floor(size / k)
        df_sharpe_ratio_cluster.sort_values(by=['Volatility'], inplace=True)
        for cluster in df_sharpe_ratio_cluster['cluster']:
            selected_assets = df_sharpe_ratio_cluster.groupby('cluster').apply(
                    lambda x: x.nsmallest(amount, 'Volatility')).reset_index(drop=True)