import pytest
from scripts.deploy import deploy
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import OtherDeedClone, network


@pytest.fixture
def get_contract():
    deployer_account = get_account()
    other_deed_clone = OtherDeedClone.deploy({"from": deployer_account})
    return other_deed_clone, deployer_account


@pytest.fixture
def skip_live_testing():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
