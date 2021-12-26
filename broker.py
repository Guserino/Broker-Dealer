import pandas as pd 
import user
import accounts as act 
#class broker:

def market_rate(crypto):
	spot_rates = pd.read_excel('spot_rates.xlsx','spot_rates')
	value = spot_rates.loc[spot_rates['Crypto'] == crypto].iloc[0][1]
	return value

def broker_wallet():
	df = pd.read_excel('spot_rates.xlsx','broker_balances')
	return df

