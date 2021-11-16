import pytest
from brownie import network, accounts, exceptions
from scripts.utils import *
from scripts.deploy import deploy_fund_me


def test_can_fund_and_withdraw():
    """测试"""
    account = get_account()
    fund_me = deploy_fund_me()
    # entrace fee 入场费
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    """测试是否只有合约创建则才能转账"""
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # 不是本地网络，则跳过测试
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # 非合约创建者，转账会失败，而失败是我们期望的结果，所以使用pytest.raises将其包裹
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
