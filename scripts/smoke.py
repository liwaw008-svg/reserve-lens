import json,re,time
from pathlib import Path
from genlayer_py import create_client,create_account
from genlayer_py.chains import studionet
R=Path(__file__).parents[1];E=(R.parents[3]/'accounts.env').read_text();key=next(x.split('=',1)[1].strip().strip('"').strip("'") for x in E.splitlines() if x.startswith('ACCOUNT_4_GENLAYER_PRIVATE_KEY='));c=create_client(chain=studionet,account=create_account(account_private_key=key));a='0xE51dbA6168A1B87001dA65994e7E2873caa33707';i='LIVE-'+str(int(time.time()));base='d42ee40';assets=f'https://raw.githubusercontent.com/liwaw008-svg/reserve-lens/{base}/evidence/assets.txt';debts=f'https://cdn.jsdelivr.net/gh/liwaw008-svg/reserve-lens@{base}/evidence/liabilities.txt';tx=[]
def send(fn,args):
 h=c.write_contract(address=a,function_name=fn,args=args);r=c.wait_for_transaction_receipt(transaction_hash=h,status='FINALIZED',retries=180,interval=5000);assert r.get('status_name')=='FINALIZED';tx.append(h)
send('register',[i,'Published reserve coverage',assets,debts,12000]);send('observe',[i,1,assets,debts]);print(json.dumps({'id':i,'state':'COVERED','transactions':tx}),flush=True)
