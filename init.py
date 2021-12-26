import accounts as act 
import user
import broker as bk

#def initialize_broker():
broker = user.user('Broker')
broker.accounts['crypto'] = act.account('0x790uf08h787136h108')
df = bk.broker_wallet()
for row in range(len(df)):
	broker.accounts['crypto'].holdings[str(df.iloc[row][0])] = df.iloc[row][1]		
#initialize_broker()



rav = user.user('guserino')
rav.accounts['crypto'] = act.account('0x7n289h9868631fb712')
rav.accounts['crypto'].modify_holdings(1,'Ethereum',650)
rav.accounts['crypto'].modify_holdings(1,'Algorand',350)



#rav.add_account('crypto_wallet')
