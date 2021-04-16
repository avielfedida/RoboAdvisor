import pandas as pd
import numpy as np
from algorithms.Algorithm import Algorithm
from datetime import datetime, timedelta


class Gini(Algorithm):

    def __init__(self, risk_score, model_name):
        super().__init__( risk_score, model_name )

    def get_optimal_portfolio(self):
        selected_prices_value = self.prices_df[self.selected_assets].dropna()
        num_portfolios = 1000
        years = len(selected_prices_value) / 253
        starting_value = selected_prices_value.iloc[0, :]
        ending_value = selected_prices_value.iloc[len(selected_prices_value) - 1, :]
        total_period_return = ending_value / starting_value
        annual_returns = (total_period_return ** (1 / years)) - 1
        port_returns = []
        port_gini_coefficient = []
        sharpe_ratio = []
        stock_weights = []
        num_assets = len(self.selected_assets)
        np.random.seed(101)

        for single_portfolio in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            returns = np.dot(weights, annual_returns)
            gini_coefficient = (selected_prices_value.mad()).mad()
            sharpe = returns / gini_coefficient
            sharpe_ratio.append(sharpe)
            port_returns.append(returns * 100)
            port_gini_coefficient.append(gini_coefficient * 100)
            stock_weights.append(weights)
        portfolio = {'Returns': port_returns,
                     'Volatility': port_gini_coefficient,
                     'Sharpe Ratio': sharpe_ratio}
        for i, symbol in enumerate(self.selected_assets):
            portfolio[symbol] = [Weight[i] for Weight in stock_weights]
        df = pd.DataFrame(portfolio)
        columns = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock for stock in self.selected_assets]
        df = df[columns]
        best_sharpe_portfolio = df.loc[df['Sharpe Ratio'] == df['Sharpe Ratio'].max()]
        sharpe_portfolio = pd.DataFrame(columns=['Ticker', 'Weight'])
        for i in range(len(self.selected_assets)):
            ticker = self.selected_assets[i]
            weight = best_sharpe_portfolio.loc[:, ticker].iloc[0]
            sharpe_portfolio = sharpe_portfolio.append({'Ticker': ticker, 'Weight': weight}, ignore_index=True)
        sharpe_portfolio = sharpe_portfolio.set_index('Ticker')
        return sharpe_portfolio
