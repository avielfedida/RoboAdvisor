from app.extensions import db
from app.factory import create_app
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


class Algorithm:

    def __init__(self, risk_score):
        app = create_app()
        app.app_context().push()
        self.risk_score = risk_score
        self.all_assets = self.get_all_assets()
        self.prices_df = self.get_assets_price_data_from_db()
        self.selected_assets = self.get_selected_assets(self.risk_score)

    def get_all_assets(self):
        bonds_df = pd.read_csv('./resources/bonds_list.csv')
        sp500_stocks_df = pd.read_csv('./resources/stocks_list.csv')
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
        std_df = pd.DataFrame(index=self.prices_df.columns, columns=['std'])
        for index, asset in enumerate(self.prices_df.columns):
            std_df.loc[asset, 'std'] = all_std[index]
        std_df.sort_values(by=['std'], inplace=True)

        # return the relevant assets according to the risk level
        size = int(len(std_df) / 5)
        if risk_score == 1:
            selected_assets = std_df.iloc[0:size].index.tolist()
        elif risk_score == 2:
            selected_assets = std_df.iloc[size:size * 2].index.tolist()
        elif risk_score == 3:
            selected_assets = std_df.iloc[size * 2:size * 3].index.tolist()
        elif risk_score == 4:
            selected_assets = std_df.iloc[size * 3:size * 4].index.tolist()
        elif risk_score == 5:
            selected_assets = std_df.iloc[size * 4:size * 5].index.tolist()
        else:
            selected_assets = std_df.index.tolist()
        return selected_assets

    def get_optimal_portfolio(self, score):
        pass

    @staticmethod
    def create_model(model_name, risk):
        if model_name == 'markowitz':
            return Markowitz(risk)
        # todo add more models

    def build_portfolio(self):
        return self.get_optimal_portfolio(self.risk_score)


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


algo = Algorithm.create_model('markowitz', 1)
algo.get_assets_price_data_from_db()
portfolio = algo.build_portfolio()
print(portfolio)
print('done')