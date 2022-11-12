import pytest
from scripts.deploy import deploy
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import OtherDeedClone, network, ExposedOtherDeedClone


@pytest.fixture
def get_contract():
    deployer_account = get_account()
    other_deed_clone = OtherDeedClone.deploy({"from": deployer_account})
    return other_deed_clone, deployer_account


@pytest.fixture
def skip_live_testing():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")


@pytest.fixture
def get_exposed_contract():
    deployer_account = get_account()
    exposed_other_deed_clone = ExposedOtherDeedClone.deploy({"from": deployer_account})
    return exposed_other_deed_clone, deployer_account


@pytest.fixture
def skip_local_testing():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for live testing!")
