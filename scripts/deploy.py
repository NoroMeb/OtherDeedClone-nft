from scripts.helpful_scripts import get_account
from brownie import OtherDeedClone

METADATA_BASE_URI = "ipfs://QmXzjCbk1u8E1xdDn7YDx5773VZuBk4wVtipfdmmeHcnLc/"


def main():
    deploy()


def deploy():
    account = get_account()
    other_deed_clone = OtherDeedClone.deploy({"from": account})
    return other_deed_clone
