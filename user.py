
class user():
	def __init__(self,name,accounts={}):
		self.name = name
		self.accounts = accounts
		self.accounts['Cash'] = 0

	def add_account(self,account_name):
		self.accounts[account_name]
	def delete_account(self,account_name):
		del self.accounts[account_name]
	def account_xsfr(self,account_name,counterparty):
		counterparty.add_account(account_name)
		self.delete_account(account_name)




