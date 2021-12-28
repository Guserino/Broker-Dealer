import accounts as act 
import user
import broker as bk
from actions import action
import pandas as pd
pd.set_option('display.max_columns', None)
pd. get_option("display.max_columns") 
pd.set_option('display.width', 150)
rav = user.user('guserino')
rav.accounts['crypto'] = act.account('0x7n2',{},'Premium')
wallet = rav.accounts['crypto']
rav.accounts['cryptov2'] = act.account('0x797',{},'Premium')
wallet_alt = rav.accounts['cryptov2']

action.add_withdraw_funds(wallet,'Add',5000)
action.buy(wallet,'Ethereum',.06)
#print(wallet.holdings)
action.buy(wallet,'Algorand',15,'Ethereum')
action.transfer(wallet,'Algorand',12,wallet_alt)
action.sell(wallet,'Algorand',3)
action.buy(wallet,'Ethereum',2,leverage=.5)
#print(wallet.holdings)
print(bk.trade_log)
#bk.trade_log.to_excel('trade_log.xlsx')
#print(wallet.holdings)