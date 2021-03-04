import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
from datetime import datetime, timedelta

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


class Markowitz:
    all_assets = ['SHY', 'TLT', 'SHV', 'IEF', 'GOVT', 'AAPL', 'AMZN', 'MSFT', 'GOOG', 'NFLX']

    end_date = datetime.now() - timedelta(1)
    start_date = datetime(end_date.year - 1, end_date.month, end_date.day)
    # prices_df = pd.DataFrame()
    #TODO: FIX HERE, FIX PATHS
    # prices_df = pd.read_excel('./resources/assets_prices.xlsx', index_col=0)
    selected_assets = []

    def get_all_assets(self):
        bonds = pd.read_html('https://etfdb.com/etfdb-category/government-bonds')
        bonds_df = bonds[0]['Symbol'].iloc[0:25]
        sp500_stocks = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        sp500_stocks_df = sp500_stocks[0]['Symbol']
        self.all_assets = bonds_df.tolist() + sp500_stocks_df.tolist()
        bonds_df.to_excel('bonds list.xlsx')
        sp500_stocks_df.to_excel('stocks list.xlsx')

    def get_assets_price_data(self):
        price_data = {}
        for asset in self.all_assets:
            print(asset)
            try:
                data_var = pdr.get_data_yahoo(asset, self.start_date, self.end_date)['Adj Close']
                data_var.to_frame()
                price_data.update({asset: data_var})
            except:
                print("failed")
                self.all_assets.remove(asset)
                continue
        self.prices_df = pd.DataFrame(price_data)
        self.prices_df.to_excel('./resources/assets_prices.xlsx')
        pd.DataFrame(self.all_assets).to_excel('./resources/assets_list.xlsx')

    def get_selected_assets(self, risk_score):
        # self.get_assets_price_data()
        print(len(self.prices_df.columns))
        all_std = [self.prices_df[col].std() for col in self.prices_df.columns]
        print(len(all_std))
        print(len(self.all_assets))
        std_df = pd.DataFrame(index=self.prices_df.columns, columns=['std'])
        for index, asset in enumerate(self.all_assets):
            print(asset)
            std_df.loc[asset, 'std'] = all_std[index]
        std_df.sort_values(by=['std'], inplace=True)

        # return the relevant assets according to the risk level
        size = int(len(std_df) / 5)
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
        self.get_selected_assets(score)
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
        fig = self.pie_plot(sharpe_portfolio)
        # self.plot_portfolios( df )
        return fig

    def pie_plot(self, portfolio):
        portfolio.columns = portfolio.columns.str.rstrip(' Weight')
        assets_list = portfolio.columns[3:].tolist()
        bonds_list = pd.read_excel('./resources/bonds_list.xlsx')['Symbol'].tolist()
        port_bonds_list = list(set(assets_list).intersection(set(bonds_list)))
        port_stocks_list = list(set(assets_list) ^ set(port_bonds_list))
        bonds_weights = portfolio.loc[:, port_bonds_list].iloc[0].tolist()
        stocks_weights = portfolio.loc[:, port_stocks_list].iloc[0].tolist()
        fig, (ax2, ax1, ax3) = plt.subplots(1, 3, dpi=150, figsize=(20, 12))

        # build ratio graph
        ratio_labels = ['bonds', 'stocks']
        portfolio_build_size = [sum(bonds_weights), sum(stocks_weights)]
        ax1.pie(portfolio_build_size, labels=ratio_labels, autopct='%0.1f%%', startangle=90, labeldistance=1.05)
        # ax1.set_title('יחס בין מניות לאיגרות חוב')
        # build bonds graph
        ax2.pie(bonds_weights, labels=port_bonds_list, autopct='%0.1f%%', startangle=90, labeldistance=1.05)
        # ax2.set_title('חלוקת איגרות החוב')
        # build stocks graph
        patches, texts, autotexts = ax3.pie(stocks_weights, labels=port_stocks_list, autopct='%0.1f%%', startangle=330, labeldistance=1.25)
        for txt in texts:
            txt.set_fontsize(8)
        # ax3.set_title('חלוקת המניות')
        # plt.text(0, 0, (u'תיק ההשקעות המומלץ')[::-1], name='Arial', horizontalalignment='center', verticalalignment='top')
        # results = 'Portfolio Return: ' + str(100) + ' Portfolio Volatility: ' + str(100) + ' Portfolio Sharpe Ratio: ' + str(100)
        # plt.text( 0, 0.5, results )
        # plt.show()

        return fig

    def plot_portfolios(self, df):
        min_volatility = df['Volatility'].min()
        max_sharpe = df['Sharpe Ratio'].max()
        max_return = df['Returns'].max()
        max_vol = df['Volatility'].max()
        sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
        min_variance_port = df.loc[df['Volatility'] == min_volatility]
        max_returns = df.loc[df['Returns'] == max_return]
        max_vols = df.loc[df['Volatility'] == max_vol]
        plt.style.use('seaborn-dark')
        df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
                        cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
        plt.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'], c='green', marker='D', s=200)
        plt.scatter(x=min_variance_port['Volatility'], y=min_variance_port['Returns'], c='orange', marker='D', s=200)
        plt.scatter(x=max_vols['Volatility'], y=max_returns['Returns'], c='red', marker='D', s=200)
        plt.style.use('seaborn-dark')
        plt.xlabel('Volatility (Std. Deviation) Percentage %')
        plt.ylabel('Expected Returns Percentage %')
        plt.title('Efficient Frontier')
        plt.subplots_adjust(bottom=0.4)
        red_num = df.index[df["Returns"] == max_return]
        yellow_num = df.index[df['Volatility'] == min_volatility]
        green_num = df.index[df['Sharpe Ratio'] == max_sharpe]
        multseries = pd.Series([1, 1, 1] + [100 for stock in self.selected_assets],
                               index=['Returns', 'Volatility', 'Sharpe Ratio'] + [stock + ' Weight' for stock in
                                                                                  self.selected_assets])
        with pd.option_context('display.float_format', '%{:,.2f}'.format):
            plt.figtext(0.2, 0.15, "Max returns Porfolio: \n" + df.loc[red_num[0]].multiply(multseries).to_string(),
                        bbox=dict(facecolor='red', alpha=0.5), fontsize=11, style='oblique', ha='center',
                        va='center',
                        wrap=True)
            plt.figtext(0.45, 0.15, "Safest Portfolio: \n" + df.loc[yellow_num[0]].multiply(multseries).to_string(),
                        bbox=dict(facecolor='yellow', alpha=0.5), fontsize=11, style='oblique', ha='center',
                        va='center',
                        wrap=True)
            plt.figtext(0.7, 0.15, "Sharpe  Portfolio: \n" + df.loc[green_num[0]].multiply(multseries).to_string(),
                        bbox=dict(facecolor='green', alpha=0.5), fontsize=11, style='oblique', ha='center',
                        va='center',
                        wrap=True)
        plt.savefig('portfolio.png')

    def remove_noise_data(self):
        assets = self.all_assets['Symbol'].tolist()
        for asset in self.prices_df.columns:
            if asset not in assets:
                del self.prices_df[asset]
        for asset in self.all_assets['Symbol']:
            if asset not in self.prices_df.columns:
                assets.remove(asset)
        self.all_assets = pd.DataFrame(assets, columns=['Symbol'])
