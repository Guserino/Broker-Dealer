import pandas as pd  
#class broker:

def market_rate(crypto):
	spot_rates = pd.read_excel('spot_rates.xlsx','spot_rates')
	value = spot_rates.loc[spot_rates['Crypto'] == crypto].iloc[0][1]
	return value

class broker():
	def __init__(self,holdings={}):
		self.holdings = holdings
		df = pd.read_excel('spot_rates.xlsx','broker_balances')
		for row in range(len(df)):
			self.holdings[str(df.iloc[row][0])] = df.iloc[row][1]

broker = broker()
print('RAV Securities LLC. - Holdings:')
print(broker.holdings)