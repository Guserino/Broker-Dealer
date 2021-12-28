import broker as bk 
import user
import pandas as pd
class account():
	def __init__(self,address,holdings,account_type='Regular'):
		self.address = address
		self.holdings = holdings
		self.account_type = account_type if account_type is not None else 'Premium'
		if account_type == 'Premium':
			self.holdings['Margin'] = 0


