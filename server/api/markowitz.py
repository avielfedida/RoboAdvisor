import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
from datetime import datetime, timedelta

pd.set_option( 'display.max_rows', None )
pd.set_option( 'display.max_columns', None )
pd.set_option( 'display.width', None )


class Markowitz:
    all_assets = ['SHY', 'TLT', 'SHV', 'IEF', 'GOVT', 'AAPL', 'AMZN', 'MSFT', 'GOOG', 'NFLX']
    end_date = datetime.now() - timedelta( 1 )
    start_date = datetime( end_date.year - 1, end_date.month, end_date.day )
    prices_df = pd.DataFrame()
    selected_assets = []

    def get_all_assets(self):
        bonds = pd.read_html( 'https://etfdb.com/etfdb-category/government-bonds' )
        bonds_df = bonds[0]['Symbol'].iloc[0:25]
        sp500_stocks = pd.read_html( 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies' )
        sp500_stocks_df = sp500_stocks[0]['Symbol']
        self.all_assets = bonds_df.tolist() + sp500_stocks_df.tolist()
        bonds_df.to_excel( 'bonds list.xlsx' )
        sp500_stocks_df.to_excel( 'stocks list.xlsx' )

    def get_assets_price_data(self):
        price_data = {}
        counter = 0
        for asset in self.all_assets:
            print( asset )
            print( counter + 1 )
            counter += 1
            try:
                data_var = pdr.get_data_yahoo( asset, self.start_date, self.end_date )['Adj Close']
                data_var.to_frame()
                price_data.update( {asset: data_var} )
            except:
                self.all_assets.remove( asset )
                continue
        self.prices_df = pd.DataFrame( price_data )
        self.prices_df.to_excel( 'assets_prices.xlsx' )
        pd.DataFrame( self.all_assets ).to_excel( 'assets_list.xlsx' )

    def select_assets(self, risk_score):
        all_std = [self.prices_df[col].std() for col in self.prices_df.columns]
        std_df = pd.DataFrame( index=self.prices_df.columns, columns=['std'] )
        for index, asset in enumerate( self.all_assets ):
            std_df.loc[asset, 'std'] = all_std[index]
        std_df.sort_values( by=['std'], inplace=True )

        # return the relevant assets according to the risk level
        selected_assets = pd.DataFrame()
        size = int( len( std_df ) / 5 )
        if risk_score == 1:
            self.selected_assets = std_df.iloc[0:size].index.tolist()
        elif risk_score == 2:
            self.selected_assets = std_df.iloc[size:size * 2].index.tolist()
        elif risk_score == 3:
            self.selected_assets = std_df.iloc[size * 2:size * 3].index.tolist()
        elif risk_score == 4:
            self.selected_assets = std_df.iloc[size * 3:size * 4].index.tolist()
        elif risk_score == 5:
            self.selected_assets = std_df.iloc[size * 4:size * 5].index.tolist()
        else:
            self.selected_assets = std_df.index.tolist()
        return

    def get_optimal_portfolio(self, score):
        model.selected_assets(score)
        selected_prices_value = self.prices_df[self.selected_assets].dropna()
        num_portfolios = 500
        years = len( selected_prices_value ) / 253
        starting_value = selected_prices_value.iloc[0, :]
        ending_value = selected_prices_value.iloc[len( selected_prices_value ) - 1, :]
        total_period_return = ending_value / starting_value
        annual_returns = (total_period_return ** (1 / years)) - 1
        annual_covariance = selected_prices_value.pct_change().cov() * 253
        port_returns = []
        port_volatility = []
        sharpe_ratio = []
        stock_weights = []
        num_assets = len( self.selected_assets )
        np.random.seed( 101 )

        for single_portfolio in range( num_portfolios ):
            weights = np.random.random( num_assets )
            weights /= np.sum( weights )
            returns = np.dot( weights, annual_returns )
            volatility = np.sqrt( np.dot( weights.T, np.dot( annual_covariance, weights ) ) )
            sharpe = returns / volatility
            sharpe_ratio.append( sharpe )
            port_returns.append( returns * 100 )
            port_volatility.append( volatility * 100 )
            stock_weights.append( weights )
        portfolio = {'Returns': port_returns,
                     'Volatility': port_volatility,
                     'Sharpe Ratio': sharpe_ratio}
        for counter, symbol in enumerate( self.selected_assets ):
            portfolio[symbol + ' Weight'] = [Weight[counter] for Weight in stock_weights]
        df = pd.DataFrame( portfolio )
        column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock + ' Weight' for stock in self.selected_assets]
        df = df[column_order]
        sharpe_portfolio = df.loc[df['Sharpe Ratio'] == df['Sharpe Ratio'].max()]
        fig = self.pie_plot( sharpe_portfolio )
        return fig

    def pie_plot(self, portfolio):
        portfolio.columns = portfolio.columns.str.rstrip( ' Weight' )
        labels = portfolio.columns[3:]
        sizes = portfolio.iloc[0][3:].tolist()
        fig, ax1 = plt.subplots()
        ax1.pie( sizes, labels=labels, autopct='%0.1f%%', startangle=90 )
        ax1.axis( 'equal' )
        # plt.show()
        return fig

    # def remove_noise_data(self):
    #     assets = self.all_assets['Symbol'].tolist()
    #     for asset in self.prices_df.columns:
    #         if asset not in assets:
    #             del self.prices_df[asset]
    #     for asset in self.all_assets['Symbol']:
    #         if asset not in self.prices_df.columns:
    #             assets.remove(asset)
    #     self.all_assets = pd.DataFrame(assets, columns=['Symbol'])


# model = Markowitz()
# model.get_all_assets()
# model.get_assets_price_data()
# model.all_assets = pd.read_excel('stocks_list.xlsx', index_col=0)
# model.prices_df = pd.read_excel('assets prices.xlsx', index_col=0)
# model.remove_noise_data()
# model.select_assets()
# model.get_optimal_portfolio(0)
