from scripts.helpful_scripts import get_account
from web3 import Web3
from brownie import config, accounts

RECEIVER_ACCT = accounts.add(config["wallets"]["from_key_2"])

METADATA_BASE_URI = "ipfs://QmXzjCbk1u8E1xdDn7YDx5773VZuBk4wVtipfdmmeHcnLc/"


def test_can_mint_and_withdraw(skip_local_testing, get_contract):
    # Arrange
    skip_local_testing
    other_deed_clone, deployer_account = get_contract
    public_mint_open = True
    allow_lis_mint_open = True
    public_minter = get_account()
    allowed_minter = get_account()
    allowed_list = [allowed_minter]
    public_price = Web3.toWei(0.01, "ether")
    allowed_list_price = Web3.toWei(0.001, "ether")
    receiver = RECEIVER_ACCT
    receiver_initial_balance = receiver.balance()
    # Act
    other_deed_clone._setBaseURI(METADATA_BASE_URI, {"from": deployer_account})
    other_deed_clone.editMintWindows(
        public_mint_open, allow_lis_mint_open, {"from": deployer_account}
    )
    other_deed_clone.setAllowList(allowed_list, {"from": deployer_account})
    other_deed_clone.publicMint({"from": public_minter, "value": public_price})
    other_deed_clone.allowListMint(
        {"from": allowed_minter, "value": allowed_list_price}
    )
    other_deed_clone.withdraw(receiver, {"from": deployer_account})

    # Assert
    assert other_deed_clone.ownerOf(0) == public_minter
    assert other_deed_clone.ownerOf(1) == allowed_minter
    assert (
        receiver.balance()
        == receiver_initial_balance + public_price + allowed_list_price
    )
