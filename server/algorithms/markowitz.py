import pandas as pd
import numpy as np
from algorithms.Algorithm import Algorithm
from datetime import datetime, timedelta


class Markowitz(Algorithm):

    def __init__(self, risk_score):
        super().__init__( risk_score )
        self.all_assets = ['SHY', 'TLT', 'SHV', 'IEF', 'GOVT', 'AAPL', 'AMZN', 'MSFT', 'GOOG', 'NFLX']
        self.end_date = datetime.now() - timedelta(1)
        self.start_date = datetime(self.end_date.year - 1, self.end_date.month, self.end_date.day)

    def get_optimal_portfolio(self, score):
        selected_prices_value = self.prices_df[self.selected_assets].dropna()
        num_portfolios = 500
        years = len(selected_prices_value) / 253
        starting_value = selected_prices_value.iloc[0, :]
        ending_value = selected_prices_value.iloc[len(selected_prices_value) - 1, :]
        total_period_return = ending_value / starting_value
        annual_returns = (total_period_return ** (1 / years)) - 1
        annuanl_covariance = selected_prices_value.pct_change().cov() * 253
        port_returns = []
        port_volatility = []
        sharpe_ratio = []
        stock_weights = []
        num_assets = len(self.selected_assets)
        np.random.seed(101)

        for single_portfolio in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            returns = np.dot(weights, annual_returns)
            volatility = np.sqrt(np.dot(weights.T, np.dot(annuanl_covariance, weights)))
            sharpe = returns / volatility
            sharpe_ratio.append(sharpe)
            port_returns.append(returns * 100)
            port_volatility.append(volatility * 100)
            stock_weights.append(weights)
        portfolio = {'Returns': port_returns,
                     'Volatility': port_volatility,
                     'Sharpe Ratio': sharpe_ratio}
        for counter, symbol in enumerate(self.selected_assets):
            portfolio[symbol + ' Weight'] = [Weight[counter] for Weight in stock_weights]
        df = pd.DataFrame(portfolio)
        column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock + ' Weight' for stock in self.selected_assets]
        df = df[column_order]
        sharpe_portfolio = df.loc[df['Sharpe Ratio'] == df['Sharpe Ratio'].max()]
        return sharpe_portfolio.to_json()

    def remove_noise_data(self):
        assets = self.all_assets['Symbol'].tolist()
        for asset in self.prices_df.columns:
            if asset not in assets:
                del self.prices_df[asset]
        for asset in self.all_assets['Symbol']:
            if asset not in self.prices_df.columns:
                assets.remove(asset)
        self.all_assets = pd.DataFrame(assets, columns=['Symbol'])


# algo = Algorithm.create_model('markowitz', 1)
# algo.get_assets_price_data_from_db()
# portfolio = algo.build_portfolio()
# print(portfolio)
# print('done')