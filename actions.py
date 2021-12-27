import broker as bk
class action():

	def buy(self,security_name,amount,purchasing_currency='Cash'):
		assert (amount >= 0)
		if security_name not in self.holdings:
			self.holdings[security_name] = 0
		if amount <= self.holdings[purchasing_currency] and amount/bk.market_rate(security_name) <= bk.broker.holdings[security_name]:
			self.holdings[purchasing_currency] -= amount
			amount *= bk.market_rate(purchasing_currency)
			self.holdings[security_name] += amount/bk.market_rate(security_name)
			bk.broker.holdings[security_name] -= amount/bk.market_rate(security_name)
			amount /= bk.market_rate(purchasing_currency)
			bk.broker.holdings[purchasing_currency] += amount
		else:
			raise Exception("Transaction unsuccesful")

	def sell(self,security_name,amount):
		assert (amount >= 0)
		if amount <= self.holdings[security_name] and bk.broker.holdings['Cash'] >= amount*bk.market_rate(security_name):
			self.holdings['Cash'] += amount*bk.market_rate(security_name)
			self.holdings[security_name] -= amount/bk.market_rate(security_name)
			bk.broker.holdings[security_name] += amount/bk.market_rate(security_name)
			bk.broker.holdings['Cash'] -= amount			
		else:
			raise Exception("Transaction unsuccesful")
	
	def transfer(self,security_name,amount,counterparty):
		assert (amount >= 0)
		if amount <= self.holdings[security_name]:
			if security_name not in counterparty.holdings:
				counterparty.holdings[security_name] = 0
			self.holdings[security_name] -= amount/bk.market_rate(security_name)
			counterparty.holdings[security_name] += amount/bk.market_rate(security_name)	

	def add_withdraw_funds(self,action,amount):
		assert (amount >= 0)
		if action == 'add':
			self.holdings['Cash'] += amount
		if action == 'withdraw' and amount <= self.holdings['Cash']:
			self.holdings['Cash'] -= amount


	#def modify_funds():
