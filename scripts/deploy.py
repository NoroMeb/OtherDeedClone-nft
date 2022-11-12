from scripts.helpful_scripts import get_account
from brownie import OtherDeedClone


def main():
    deploy()


def deploy():
    account = get_account()
    other_deed_clone = OtherDeedClone.deploy({"from": account}, publish_source=True)
    print(other_deed_clone.address)
    return other_deed_clone
