from app.extensions import db
import pandas as pd
import numpy as np
import scipy.optimize
from algorithms.Algorithm import Algorithm
from models.portfolio_stocks import PortfolioStocks
from models.stock_price import StockPrice
from datetime import datetime
from datetime import datetime

class BlackLitterman(Algorithm):

    def __init__(self, risk_score, model_name):
        super().__init__(risk_score, model_name)
        self.df_cap_bonds_and_stocks = pd.DataFrame(columns=['ticker', 'market_cap'])
        dates = self.prices_df.index
        self.df_prices_bonds_and_stocks = pd.DataFrame(index=dates, columns=self.selected_assets)
        self.set_dfs()
        self.n = len(self.selected_assets)

    def set_dfs(self):
        self.df_cap_bonds_and_stocks = pd.DataFrame(columns=['ticker', 'market_cap'])
        data = pd.read_sql_table('stocks_prices', db.engine)
        data['date_time'] = pd.to_datetime(data['date_time'])
        len_df = len(self.df_prices_bonds_and_stocks.index)

        for ticker in self.selected_assets:
            last_date = data[data['ticker'] == ticker]['date_time'].max()
            market_cap_ti = data[data['ticker'] == ticker]
            market_cap = market_cap_ti[market_cap_ti['date_time'] == last_date].iloc[0]['market_cap']
            self.df_cap_bonds_and_stocks = self.df_cap_bonds_and_stocks.append(
                {'ticker': ticker, 'market_cap': market_cap}, ignore_index=True)
            self.df_prices_bonds_and_stocks[ticker] = data[data['ticker'] == ticker]['price'].iloc[-len_df:].values

    # Calculates portfolio mean return
    def port_mean(self, weights, returns):
        return sum(returns * weights)

    # Calculates portfolio variance of returns
    def port_var(self, weights, covariance_matrix):
        return np.dot(np.dot(weights, covariance_matrix), weights)

    # Combination of the two functions above - mean and variance of returns calculation
    def port_mean_var(self, weights, returns, covariance_matrix):

        return self.port_mean(weights, returns), self.port_var(weights, covariance_matrix)

    # Given risk-free rate, assets returns and covariances, this function calculates
    # mean-variance frontier and returns its [x,y] points in two arrays
    def solve_frontier(self, returns, covariance_matrix):
        def fitness(weights_fit, returns_fit, covariance_matrix_fit, r):
            # For given level of return r, find weights which minimizes portfolio variance.
            mean, var = self.port_mean_var(weights_fit, returns_fit, covariance_matrix_fit)
            # Big penalty for not meeting stated portfolio return effectively serves as optimization constraint
            penalty = 100 * abs(mean - r)
            return var + penalty

        frontier_mean, frontier_var, frontier_weights = [], [], []
        n = len(returns)  # Number of assets in the portfolio
        for r in np.linspace(min(returns), max(returns), num=20):  # Iterate through the range of returns on Y axis
            weights = np.ones([n]) / n  # start optimization with equal weights
            b_ = [(0, 1) for i in range(n)]
            c_ = ({'type': 'eq', 'fun': lambda weights: sum(weights) - 1.})
            optimized = scipy.optimize.minimize(fitness, weights, (returns, covariance_matrix, r),
                                                method='SLSQP', constraints=c_, bounds=b_)
            # if not optimized.success:
            #     raise BaseException(optimized.message)
            # add point to the efficient frontier [x,y] = [optimized.x, r]
            frontier_mean.append(r)
            frontier_var.append(self.port_var(optimized.x, covariance_matrix))
            frontier_weights.append(optimized.x)
        return np.array(frontier_mean), np.array(frontier_var), frontier_weights

    # Function takes historical stock prices together with market capitalizations and
    # calculates weights, historical returns and historical covariances
    def assets_historical_returns_and_covariances(self, prices):
        prices_mat = np.matrix(prices)  # create numpy matrix from prices
        # create matrix of historical returns
        rows, cols = prices_mat.shape
        returns = np.empty([rows, cols - 1])
        for r in range(rows):
            for c in range(cols - 1):
                p0, p1 = prices_mat[r, c], prices_mat[r, c + 1]
                returns[r, c] = (p1 / p0) - 1
        # calculate returns
        expreturns = np.array([])
        for r in range(rows):
            expreturns = np.append(expreturns, np.mean(returns[r]))
        # calculate covariances
        covars = np.cov(returns)
        expreturns = (1 + expreturns) ** 250 - 1  # Annualize returns
        covars = covars * 250  # Annualize covariances
        return expreturns, covars

    # Given risk-free rate, assets returns and covariances, this function calculates
    # weights of tangency portfolio with respect to sharpe ratio maximization
    def solve_weights(self, returns, covariance_matrix, risk_free_rate):
        def fitness(weights_fit, returns_fit, covariance_matrix_fit, risk_free_rate_fit):
            # calculate mean/variance of the portfolio
            mean, var = self.port_mean_var(weights_fit, returns_fit, covariance_matrix_fit)
            # utility = Sharpe ratio
            util = (mean - risk_free_rate_fit) / np.sqrt(var)
            # maximize the utility, minimize its inverse value
            return 1 / util

        n = len(returns)
        # start optimization with equal weights
        weights = np.ones([n]) / n
        # weights for boundaries between 0%..100%. No leverage, no shorting
        b_ = [(0., 1.) for i in range(n)]
        # Sum of weights must be 100%
        c_ = ({'type': 'eq', 'fun': lambda weights: sum(weights) - 1.})
        optimized = scipy.optimize.minimize(fitness, weights, (returns, covariance_matrix, risk_free_rate),
                                            method='SLSQP', constraints=c_, bounds=b_)
        # if not optimized.success:
        #     raise BaseException(optimized.message)
        return optimized.x

    def optimize_frontier(self, returns, covariance_matrix, risk_free_rate):
        weights = self.solve_weights(returns, covariance_matrix, risk_free_rate)
        # calculate tangency portfolio
        tangency_mean, tangency_var = self.port_mean_var(weights, returns, covariance_matrix)
        # calculate efficient frontier
        frontier_mean, frontier_var, frontier_weights = self.solve_frontier(returns, covariance_matrix)
        # Weights, Tangency portfolio asset means and variances, Efficient frontier means and variances
        return weights, tangency_mean, tangency_var, frontier_mean, frontier_var, frontier_weights

    # def get_portfolio_object(self, model_name):
    #     algorithm_name = model_name
    #     portfolio = self.create_portfolio(self.risk_score, algorithm_name)
    #     sharpe_portfolio = self.get_optimal_portfolio()
    #     data = pd.read_sql_table('stocks_prices', db.engine)
    #     data['date_time'] = pd.to_datetime(data['date_time'])
    #     for ticker in sharpe_portfolio.index.values:
    #         last_date = data[data['ticker'] == ticker]['date_time'].max()
    #         weight = sharpe_portfolio.loc[ticker, 'Weight']
    #         portfolio_stock = PortfolioStocks(stock_price_ticker=ticker, stock_price_date_time=last_date,
    #                                           portfolio=portfolio, portfolios_date_time=datetime.now,
    #                                           portfolios_algorithm=algorithm_name, weight=weight, portfolios_risk=portfolio.risk)
    #         portfolio.portfolio_stocks.append(portfolio_stock)
    #     return portfolio

    def get_optimal_portfolio(self):
        risk_free_rate = 0.12
        prices_out = []
        for s in self.selected_assets:
            prices = list(self.df_prices_bonds_and_stocks[s])
            prices_out.append(prices)
        caps_out = [float(i) for i in list(self.df_cap_bonds_and_stocks['market_cap'])]
        sum_caps = sum(caps_out)
        # calculate market weights from capitalizations
        weights = [cap / sum_caps for cap in caps_out]
        returns, covariance_matrix = self.assets_historical_returns_and_covariances(prices_out)
        mean, var = self.port_mean_var(weights, returns, covariance_matrix)
        # Calculate risk aversion
        lmb = (mean - risk_free_rate) / var
        # Calculate equilibrium excess returns
        Pi = np.dot(np.dot(lmb, covariance_matrix), weights)
        weights, tangency_mean, tangency_var, frontier_mean, frontier_var, frontier_weights = self.optimize_frontier(Pi+risk_free_rate, covariance_matrix, risk_free_rate)
        sharpe_portfolio = pd.DataFrame(columns=['Ticker', 'Weight'])
        for i in range(len(self.selected_assets)):
            ticker = self.selected_assets[i]
            weight = weights[i]
            sharpe_portfolio = sharpe_portfolio.append({'Ticker': ticker, 'Weight': weight}, ignore_index=True)
        # return sharpe_portfolio.to_json()
        sharpe_portfolio= sharpe_portfolio.set_index('Ticker')
        return sharpe_portfolio
