import accounts as act 
import user
import broker as bk
from actions import action


rav = user.user('guserino')
rav.accounts['crypto'] = act.account('0x7n289h9868631fb712',{})
wallet = rav.accounts['crypto']
rav.accounts['cryptov2'] = act.account('0x79712597n1257hf721',{})
wallet_alt = rav.accounts['cryptov2']
action.add_withdraw_funds(wallet,'add',5000)
action.buy(wallet,'Ethereum',250)
print(wallet.holdings)
action.buy(wallet,'Algorand',.06,'Ethereum')
print(wallet.holdings)
action.transfer(wallet,'Algorand',12,wallet_alt)
print(wallet.holdings)
print(wallet_alt.holdings)
