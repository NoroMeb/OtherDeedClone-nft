from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy, METADATA_BASE_URI
import pytest
from brownie import exceptions, network
from web3 import Web3

PUBLIC_PRICE = Web3.toWei(0.01, "ether")
ALLOWED_LIST_PRICE = Web3.toWei(0.001, "ether")


def test_edit_mint_window(get_contract, skip_live_testing):
    # Arrange
    skip_live_testing
    non_owner = get_account(index=1)
    other_deed_clone, deployer_account = get_contract

    # Act
    other_deed_clone.editMintWindows(False, True, {"from": deployer_account})

    # Assert
    assert other_deed_clone.publicMintOpen() == False
    assert other_deed_clone.allowListMintOpen() == True
    with pytest.raises(exceptions.VirtualMachineError):
        other_deed_clone.editMintWindows(True, True, {"from": non_owner})


def test_set_allow_list(get_contract, skip_live_testing):
    # Arrange
    skip_live_testing
    non_owner = get_account(index=1)
    other_deed_clone, deployer_account = get_contract
    allowed_list = []
    for i in range(1):
        allowed_list.append(get_account(index=i))

    # Act
    other_deed_clone.setAllowList(allowed_list, {"from": deployer_account})

    # Assert
    for allowed_address in allowed_list:
        assert other_deed_clone.allowList(allowed_address) == True
    with pytest.raises(exceptions.VirtualMachineError):
        other_deed_clone.setAllowList(allowed_list, {"from": non_owner})

    return other_deed_clone, allowed_list


def test_allow_list_mint(get_contract, skip_live_testing):

    # Arrange
    other_deed_clone, allowed_list = test_set_allow_list(
        get_contract, skip_live_testing
    )
    deployer_account = get_contract[1]
    other_deed_clone.editMintWindows(False, True, {"from": deployer_account})
    account_allowed = allowed_list[0]
    account_not_allowed = get_account(index=2)
    not_enough_value = Web3.toWei(0.0001, "ether")

    # Act
    other_deed_clone.allowListMint(
        {"from": account_allowed, "value": ALLOWED_LIST_PRICE}
    )

    # Assert
    assert other_deed_clone.ownerOf(0) == account_allowed
    with pytest.raises(exceptions.VirtualMachineError):
        other_deed_clone.allowListMint(
            {"from": account_not_allowed, "value": ALLOWED_LIST_PRICE}
        )
    with pytest.raises(exceptions.VirtualMachineError):
        other_deed_clone.allowListMint(
            {"from": account_allowed, "value": not_enough_value}
        )

    # Arrange 2
    other_deed_clone.editMintWindows(False, False, {"from": deployer_account})

    # Act / Assert 2
    with pytest.raises(exceptions.VirtualMachineError):
        other_deed_clone.allowListMint(
            {"from": account_allowed, "value": not_enough_value}
        )
