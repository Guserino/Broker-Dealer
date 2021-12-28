import broker as bk
from datetime import date
import user
class action():

	#logs list into Broker-Dealer trade log
	def log_transaction(details):
		bk.trade_log.loc[len(bk.trade_log.index)]= details


	def buy(self,security_name,amount,purchasing_currency='Cash',leverage=0):
		
		#Conversions for purchase amount
		cash_value = amount*bk.market_rate(security_name)
		pur_cur_value = amount*bk.market_rate(security_name)/bk.market_rate(purchasing_currency)
		
		#Purchase amount must be a positive value
		assert (amount >= 0)

		#Creates space within portfolio for cryptocurrency
		if security_name not in self.holdings:
			self.holdings[security_name] = {'Margin':0,'Equity':0}

		#Checks for leveraged trades (Account premium status | margin requirements)
		if leverage != 0:
			if purchasing_currency != 'Cash':
				raise Exception('Margin trades can only take place in an cash purchase')
			if self.account_type != 'Premium' and leverage != 0:
				raise Exception('To place margin trades upgrade account to Premium status') 
					#Ensures suficient funds are available to make purchase	(both on account and broker side)
			if pur_cur_value/2 > self.holdings[purchasing_currency]['Equity'] or amount > bk.broker.holdings[security_name]:
				raise Exception("Insuficient funds")
			#margin loan trade execution
			self.holdings[security_name]['Margin'] = -cash_value/2
			self.holdings[purchasing_currency]['Equity'] -= pur_cur_value/2
			self.holdings[security_name]['Equity'] += amount
			bk.broker.holdings[security_name] -= amount
			bk.broker.holdings[purchasing_currency] += pur_cur_value/2
			bk.broker.holdings['Margin Loans'] += pur_cur_value/2

			#Logs both the client margin loan and trade
			action.log_transaction([date.today(),'Buy',self.address,'Broker-Dealer',security_name,amount,\
				purchasing_currency,amount*bk.market_rate(security_name)/bk.market_rate(purchasing_currency),\
				amount*bk.market_rate(security_name),leverage,amount*bk.market_rate(security_name)*leverage])
			action.log_transaction([date.today(),'Margin Loan','Broker-Dealer',self.address,security_name,amount,\
				purchasing_currency,amount*bk.market_rate(security_name)/bk.market_rate(purchasing_currency),\
				amount*bk.market_rate(security_name),leverage,amount*bk.market_rate(security_name)*leverage])

		#If trade is not levered procced to normal trade execution
		else:
			#Ensures suficient funds are available to make purchase	(both on account and broker side)
			if pur_cur_value > self.holdings[purchasing_currency]['Equity'] or amount > bk.broker.holdings[security_name]:
				raise Exception("Transaction unsuccesful")

			 #Trade execution
			self.holdings[purchasing_currency]['Equity'] -= pur_cur_value
			self.holdings[security_name]['Equity'] += amount
			bk.broker.holdings[security_name] -= amount
			bk.broker.holdings[purchasing_currency] += pur_cur_value
			
			#Adds transaction to Broker's ledger	
			action.log_transaction([date.today(),'Buy',self.address,'Broker-Dealer',security_name,amount,\
					purchasing_currency,amount*bk.market_rate(security_name)/bk.market_rate(purchasing_currency),\
					amount*bk.market_rate(security_name),leverage,amount*bk.market_rate(security_name)*leverage])
	


	def sell(self,security_name,amount):
		assert (amount >= 0)
		if amount <= self.holdings[security_name]['Equity'] and bk.broker.holdings['Cash'] >= amount*bk.market_rate(security_name):
			self.holdings['Cash']['Equity'] += amount*bk.market_rate(security_name)
			self.holdings[security_name]['Equity'] -= amount/bk.market_rate(security_name)
			bk.broker.holdings[security_name] += amount/bk.market_rate(security_name)
			bk.broker.holdings['Cash'] -= amount			
		else:
			raise Exception("Transaction unsuccesful")
		action.log_transaction([date.today(),'Sell',self.address,'Broker-Dealer',security_name,amount,\
				'N/A',0,amount*bk.market_rate(security_name),0,0])
	def transfer(self,security_name,amount,counterparty):
		assert (amount >= 0)
		print(amount)
		print(self.holdings[security_name]['Equity'])
		print(self.holdings[security_name]['Margin'])
		if amount <= self.holdings[security_name]['Equity'] and (self.holdings[security_name]['Margin']/\
		(self.holdings[security_name]['Margin']+self.holdings[security_name]['Equity']-amount))>.5 :
			if security_name not in counterparty.holdings:
				counterparty.holdings[security_name] = 0
			self.holdings[security_name] -= amount/bk.market_rate(security_name)
			counterparty.holdings[security_name] += amount/bk.market_rate(security_name)	
		action.log_transaction([date.today(),'Transfer',self.address,counterparty.address,security_name,amount,\
				'N/A',0,amount*bk.market_rate(security_name),0,0])
	
	def add_withdraw_funds(self,action,amount):
		assert (amount >= 0)
		if action == 'Add':
			if 'Cash' not in self.holdings:
				self.holdings['Cash'] = {}
				self.holdings['Cash']['Equity'] = 0
				self.holdings['Cash']['Margin'] = 0
			self.holdings['Cash']['Equity'] += amount
		if action == 'Withdraw' and amount <= self.holdings['Cash']:
			self.holdings.Cash.Equity -= amount
		bk.trade_log.loc[len(bk.trade_log.index)]= [date.today(),'Wire - '+action,self.address,'N/A','Cash',amount,\
				'N/A',0,0,0,0]	

'''
class action():

	def log_transaction(details):
		bk.trade_log.loc[len(bk.trade_log.index)]= details

	def buy(self,security_name,amount,purchasing_currency='Cash',leverage=0):
		assert (amount >= 0)
		if self.account_type != 'Premium' and leverage != 0:
			raise Exception('To place margin trades upgrade account to Premium status')
		if security_name not in self.holdings:
			self.holdings[security_name] = {'Margin':0,'Equity':0,'Position Value': 'Margin'+'Equity'}

		if amount*bk.market_rate(security_name)/bk.market_rate(purchasing_currency)<= self.holdings[purchasing_currency]\
		 and amount/bk.market_rate(security_name) <= bk.broker.holdings[security_name]:
			self.holdings[purchasing_currency] -= amount*bk.market_rate(security_name)/bk.market_rate(purchasing_currency)
			self.holdings[security_name] += amount
			bk.broker.holdings[security_name] -= amount
			bk.broker.holdings[purchasing_currency] += amount*bk.market_rate(security_name)/bk.market_rate(purchasing_currency)
		else:
			raise Exception("Transaction unsuccesful")
		action.log_transaction([date.today(),'Buy',self.address,'Broker-Dealer',security_name,amount,\
				purchasing_currency,amount*bk.market_rate(security_name)/bk.market_rate(purchasing_currency),\
				amount*bk.market_rate(security_name),leverage,amount*bk.market_rate(security_name)*leverage])
	



	def sell(self,security_name,amount):
		assert (amount >= 0)
		if amount <= self.holdings[security_name] and bk.broker.holdings['Cash'] >= amount*bk.market_rate(security_name):
			self.holdings['Cash'] += amount*bk.market_rate(security_name)
			self.holdings[security_name] -= amount/bk.market_rate(security_name)
			bk.broker.holdings[security_name] += amount/bk.market_rate(security_name)
			bk.broker.holdings['Cash'] -= amount			
		else:
			raise Exception("Transaction unsuccesful")
		action.log_transaction([date.today(),'Sell',self.address,'Broker-Dealer',security_name,amount,\
				'N/A',0,amount*bk.market_rate(security_name),0,0])
	def transfer(self,security_name,amount,counterparty):
		assert (amount >= 0)
		if amount <= self.holdings[security_name]:
			if security_name not in counterparty.holdings:
				counterparty.holdings[security_name] = 0
			self.holdings[security_name] -= amount/bk.market_rate(security_name)
			counterparty.holdings[security_name] += amount/bk.market_rate(security_name)	
		action.log_transaction([date.today(),'Transfer',self.address,counterparty.address,security_name,amount,\
				'N/A',0,amount*bk.market_rate(security_name),0,0])
	
	def add_withdraw_funds(self,action,amount):
		assert (amount >= 0)
		if action == 'Add':
			if 'Cash' not in self.holdings:
				self.holdings['Cash'] = 0
			self.holdings['Cash'] += amount
		if action == 'Withdraw' and amount <= self.holdings['Cash']:
			self.holdings['Cash'] -= amount
		bk.trade_log.loc[len(bk.trade_log.index)]= [date.today(),'Wire - '+action,self.address,'N/A','Cash',amount,\
				'N/A',0,0,0,0]	
'''