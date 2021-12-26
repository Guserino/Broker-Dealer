import broker as bk 
import user
class account():
	def __init__(self,address,holdings={}):
		self.address = address
		self.holdings = holdings
		self.holdings['cash'] = 1000
		#self.holdings['ethereum'] = 0
	#@staticmethod


	def modify_holdings(self,action,security_name,amount,counterparty=None):
		# 1-Purchase | 2-Withdraw| 3-Transfer Holding (pending)
		if action == 1:
			if security_name not in self.holdings:
				self.holdings[security_name] = 0
			if amount <= self.holdings['cash']:
				self.holdings['cash'] -= amount
				self.holdings[security_name] += amount/bk.market_rate(security_name)
			else:
				raise Exception("Purchase amount exceeds funds available")
		elif action == 2:
			if amount <= self.holdings[security_name]:
				self.holdings['cash'] += amount*bk.market_rate(security_name)
				self.holdings[security_name] -= amount/bk.market_rate(security_name)
			else:
				raise Exception("Withdraw amount exceeds funds available")
		elif action == 3:
			if amount <= self.holdings[security_name]:
				if security_name not in counterparty.holdings:
					counterparty.holdings[security_name] = 0
				self.holdings[security_name] -= amount/bk.market_rate(security_name)
				counterparty.holdings[security_name] += amount/bk.market_rate(security_name)
			#else:
			#	raise Exception("Transfer amount exceeds funds available")
		elif action > 3:
			raise Exception("Action not supported")
	#def account_action(self,action,security_name,amount):
	#	account.modify_holdings(self,action,security_name,amount)

