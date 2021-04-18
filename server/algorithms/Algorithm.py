import uuid

from app.extensions import db
import pandas as pd
from models.portfolio import Portfolio
from datetime import datetime
from models.portfolio_stocks import PortfolioStocks
import numpy as np

class Algorithm:

    def __init__(self, risk_score, model_name):
        self.model_name = model_name
        self.risk_score = risk_score
        self.all_assets = self.get_all_assets()
        self.prices_df = self.get_assets_price_data_from_db()
        self.selected_assets = self.get_selected_assets(self.risk_score)

    def get_all_assets(self):
        bonds_df = pd.read_csv('api/resources/bonds_list.csv')
        sp500_stocks_df = pd.read_csv('api/resources/stocks_list.csv')
        all_assets = bonds_df['Symbol'].tolist() + sp500_stocks_df['Symbol'].tolist()
        return all_assets

    def get_assets_price_data_from_db(self):
        table_data = pd.read_sql_table('stocks_prices', db.engine)
        relevant_dates = table_data['date_time'].sort_values(ascending=False).unique()[:253]  # there are approximately 253 trading days
        data = table_data[table_data['date_time'].isin(relevant_dates)]
        columns_names = data['ticker'].unique()
        dates = data['date_time'].unique()
        prices_df = pd.DataFrame(index=dates, columns=columns_names)
        for ticker in prices_df.columns:
            try:
                prices_df[ticker] = [p for p in data.loc[data['ticker'] == ticker]['price']]
            except:
                print('there is not enough data for this asset')
        prices_df.dropna(axis=1, inplace=True)
        return prices_df

    def get_selected_assets(self, risk_score):
        all_std = [self.prices_df[col].std() for col in self.prices_df.columns]
        all_ret = [self.prices_df.loc[self.prices_df.index.max(), col] - self.prices_df.loc[self.prices_df.index.min(), col] for col in self.prices_df.columns]
        all_sharpe_ratio = self.sharpe_ratio(all_ret, min(all_ret))
        std_df = pd.DataFrame(index=self.prices_df.columns, columns=['std', 'sharpe_ratio'])
        for index, asset in enumerate(self.prices_df.columns):
            std_df.loc[asset, 'std'] = all_std[index]
            std_df.loc[asset, 'sharpe_ratio'] = all_sharpe_ratio[index]
        std_df.sort_values(by=['std', 'sharpe_ratio'], inplace=True)
        take_top = 20
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

    def sharpe_ratio(self, returns, rf, days=252):
        volatility = np.array(returns).std() * np.sqrt(days)
        return (returns - rf) / volatility

    def create_portfolio(self,algorithm_name):
        date_time = datetime.now()
        # Create Portfolio Object
        uid = str(uuid.uuid4())
        portfolio = Portfolio(date_time=date_time, algorithm=algorithm_name, risk=self.risk_score, link=uid)
        return portfolio

    def get_optimal_portfolio(self):
        pass

    def get_portfolio_object(self):
        algorithm_name = self.model_name
        portfolio = self.create_portfolio(algorithm_name)
        sharpe_portfolio = self.get_optimal_portfolio()
        data = pd.read_sql_table('stocks_prices', db.engine)
        data['date_time'] = pd.to_datetime(data['date_time'])
        for ticker in sharpe_portfolio.index.values:
            last_date = data[data['ticker'] == ticker]['date_time'].max()
            weight = sharpe_portfolio.loc[ticker, 'Weight']
            portfolio_stock = PortfolioStocks(stock_price_ticker=ticker,
                                              stock_price_date_time=last_date,
                                              portfolios_id=portfolio.id,
                                              weight=weight)
            portfolio.portfolio_stocks.append(portfolio_stock)
        return portfolio


# class Markowitz(Algorithm):
#
#     def __init__(self, risk_score):
#         super().__init__( risk_score )
#         self.all_assets = ['SHY', 'TLT', 'SHV', 'IEF', 'GOVT', 'AAPL', 'AMZN', 'MSFT', 'GOOG', 'NFLX']
#         self.end_date = datetime.now() - timedelta(1)
#         self.start_date = datetime(self.end_date.year - 1, self.end_date.month, self.end_date.day)
#
#     def get_optimal_portfolio(self, score):
#         selected_prices_value = self.prices_df[self.selected_assets].dropna()
#         num_portfolios = 500
#         years = len(selected_prices_value) / 253
#         starting_value = selected_prices_value.iloc[0, :]
#         ending_value = selected_prices_value.iloc[len(selected_prices_value) - 1, :]
#         total_period_return = ending_value / starting_value
#         annual_returns = (total_period_return ** (1 / years)) - 1
#         annuanl_covariance = selected_prices_value.pct_change().cov() * 253
#         port_returns = []
#         port_volatility = []
#         sharpe_ratio = []
#         stock_weights = []
#         num_assets = len(self.selected_assets)
#         np.random.seed(101)
#
#         for single_portfolio in range(num_portfolios):
#             weights = np.random.random(num_assets)
#             weights /= np.sum(weights)
#             returns = np.dot(weights, annual_returns)
#             volatility = np.sqrt(np.dot(weights.T, np.dot(annuanl_covariance, weights)))
#             sharpe = returns / volatility
#             sharpe_ratio.append(sharpe)
#             port_returns.append(returns * 100)
#             port_volatility.append(volatility * 100)
#             stock_weights.append(weights)
#         portfolio = {'Returns': port_returns,
#                      'Volatility': port_volatility,
#                      'Sharpe Ratio': sharpe_ratio}
#         for counter, symbol in enumerate(self.selected_assets):
#             portfolio[symbol + ' Weight'] = [Weight[counter] for Weight in stock_weights]
#         df = pd.DataFrame(portfolio)
#         column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock + ' Weight' for stock in self.selected_assets]
#         df = df[column_order]
#         sharpe_portfolio = df.loc[df['Sharpe Ratio'] == df['Sharpe Ratio'].max()]
#         return sharpe_portfolio.to_json()
#
#     def remove_noise_data(self):
#         assets = self.all_assets['Symbol'].tolist()
#         for asset in self.prices_df.columns:
#             if asset not in assets:
#                 del self.prices_df[asset]
#         for asset in self.all_assets['Symbol']:
#             if asset not in self.prices_df.columns:
#                 assets.remove(asset)
#         self.all_assets = pd.DataFrame(assets, columns=['Symbol'])
#
#
# # algo = Algorithm.create_model('markowitz', 1)
# # algo.get_assets_price_data_from_db()
# # portfolio = algo.build_portfolio()
# # print(portfolio)
# # print('done')
