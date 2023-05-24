import os

from collections import defaultdict
from dotenv import load_dotenv
load_dotenv()

from pybit.unified_trading import HTTP
from pybit.exceptions import FailedRequestError


class ExBybit:
    """"""

    def __init__(self):
        self.apiKey = os.environ.get('BYBIT_API_KEY')
        self.apiSecret = os.environ.get('BYBIT_API_SECRET_KEY')
        self.session = HTTP(testnet=False, api_key=self.apiKey, api_secret=self.apiSecret)
        self.exchanger = os.path.splitext(os.path.basename(__file__))[0][3:]

    def get_account_spot(self):
        """"""
        try:
            respone = self.session.get_spot_asset_info()
            return respone
        except FailedRequestError as e:
            print(f'{self.exchanger.upper()} -- {e}')
            return {}

    def get_account_margin(self):
        """"""
        try:
            respone = self.session.get_wallet_balance(accountType="CONTRACT")
            return respone
        except FailedRequestError as e:
            print(f'{self.exchanger.upper()} -- {e}')
            return {}

    def get_account(self):
        account_spot = self.get_account_spot()
        account_margin = self.get_account_margin()
        currencies = self._normalize_data(account_spot,
                                          account_margin)
        return currencies

    def _normalize_data(self, account_spot, account_margin):
        """"""
        if not account_spot and not account_margin:
            return {self.exchanger: {}}

        q = defaultdict(list)
        if account_spot:
            for symbol in account_spot['result']['spot']['assets']:
                q[symbol['coin']].append(float(symbol['free']) + float(symbol['frozen']))

        if account_margin:
            for symbol in account_margin['result']['list'][0]['coin']:
                if symbol['coin'] in q:
                    q[symbol['coin']] = [q[symbol['coin']][0] + float(symbol['equity'])]
                else:
                    q[symbol['coin']].append(float(symbol['equity']))

        currencies = []
        for currency, value in q.items():
            currencies.append({
                'coin': currency.upper(),
                'bal': value[0]
            })
        return {self.exchanger: sorted(currencies, key=lambda x: x['coin'])}


if __name__ == '__main__':
    c = ExBybit()
    r = currencies = c.get_account()
    print(r)
