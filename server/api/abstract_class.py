import abc
import pandas as pd
from app.extensions import db


class Algorithm(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_all_assets(self):
        bonds = pd.read_html('https://etfdb.com/etfdb-category/government-bonds')
        bonds_df = bonds[0]['Symbol'].iloc[0:25]
        sp500_stocks = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        sp500_stocks_df = sp500_stocks[0]['Symbol']
        all_assets = bonds_df.tolist() + sp500_stocks_df.tolist()
        return all_assets

    @abc.abstractmethod
    def get_all_assets(self):
        bonds_df = pd.read_csv( './resources/bonds_list.csv', index=False )
        sp500_stocks_df = pd.read_csv('./resources/stocks_list.csv', index=False)
        all_assets = bonds_df.tolist() + sp500_stocks_df.tolist()
        return all_assets

    @abc.abstractmethod
    def get_assets_price_data_from_db(self):
        data = pd.read_sql_table( 'stocks_prices', db.engine )
        columns_names = data['ticker'].unique()
        dates = data['date'].unique()
        prices_df = pd.DataFrame( index=dates, columns=columns_names )
        for ticker in prices_df.columns:
            try:
                prices_df[ticker] = [p for p in data.loc[data['ticker'] == ticker]['price']]
            except:
                print( 'there is not enough data for this asset' )
        prices_df.dropna( axis=1, inplace=True )
        return prices_df

    @abc.abstractmethod
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
        pass
