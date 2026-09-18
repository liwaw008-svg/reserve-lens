from conftest import CONTRACT
def setup(vm,dep,a):vm.sender=a;x=dep(CONTRACT);x.register('lens-1','Published reserve coverage','https://assets.example/a','https://debts.example/l',12000);return x
def mock(vm):
 vm.mock_web(r'assets\.example',{'status':200,'body':'Assets 1500 date 2035-01-31'});vm.mock_web(r'debts\.example',{'status':200,'body':'Liabilities 1000 date 2035-01-31'});vm.mock_llm(r'.*ReserveLens extraction.*','{"assets":1500,"liabilities":1000,"date":"2035-01-31","consistent":true}')
def test_covered_ratio(direct_vm,direct_deploy,direct_alice):
 x=setup(direct_vm,direct_deploy,direct_alice);mock(direct_vm);x.observe('lens-1',1,'https://assets.example/a1','https://debts.example/l1');r=x.get_lens('lens-1');assert r['state']=='COVERED' and r['ratio_bps']==15000
def test_frozen_authority(direct_vm,direct_deploy,direct_alice):
 x=setup(direct_vm,direct_deploy,direct_alice);mock(direct_vm)
 with direct_vm.expect_revert('frozen authorities'):x.observe('lens-1',1,'https://other.example/a','https://debts.example/l1')
def test_forged_total_rejected(direct_vm,direct_deploy,direct_alice):
 x=setup(direct_vm,direct_deploy,direct_alice);mock(direct_vm);r=x._inspect(x.lenses['LENS-1'],'https://assets.example/a1','https://debts.example/l1');assert direct_vm.run_validator(leader_result=r);f=dict(r);f['assets']=9999;assert not direct_vm.run_validator(leader_result=f)
