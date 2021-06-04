from datetime import date
import os

apiKey=os.environ['BINANCE_API_KEY']
apiSecret=os.environ['BINANCE_API_SECRET']

from binance import Client

client = Client(apiKey, apiSecret)

print('# Coin Futures Yields')
coinfut = []
for fc in client.futures_coin_mark_price():
    if not fc['symbol'].endswith('_PERP'):
        s = fc['symbol']
        sym = s[0:-7]
        und = sym[0:-3]
        exp = s[-6:]
        exp = date(int('20'+exp[0:2]),int(exp[2:4]),int(exp[4:6]))
        mark=float(fc['markPrice'])
        index=float(fc['indexPrice'])
        coinfut.append({'sym':sym,'und':und,'exp':exp,'price':mark,'index':index})

coinfut.sort(key=lambda x:(x['sym'],x['exp']))

td = date.today()
for x in coinfut:
    r = x['price']/x['index']
    y = r ** (365/(x['exp']-td).days)
    print("{}\t{}\ty: {:f}%\tr:{:f}\tm:{:f}\ti:{:f}".format(x['und'],x['exp'],100*(y-1),r,x['price'],x['index']))

