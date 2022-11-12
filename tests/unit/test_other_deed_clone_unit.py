from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
import pytest
from brownie import exceptions, network
from web3 import Web3

PUBLIC_PRICE = Web3.toWei(0.01, "ether")
ALLOWED_LIST_PRICE = Web3.toWei(0.001, "ether")

METADATA_BASE_URI = "ipfs://QmXzjCbk1u8E1xdDn7YDx5773VZuBk4wVtipfdmmeHcnLc/"


def test_edit_mint_window(get_contract, skip_live_testing):
    # Arrange
    skip_live_testing
    non_owner = get_account(index=1)
    other_deed_clone, deployer_account = get_contract
    public_mint_open = False
    allow_list_mint_open = True

    # Act
    other_deed_clone.editMintWindows(
        public_mint_open, allow_list_mint_open, {"from": deployer_account}
    )

    # Assert
    assert other_deed_clone.publicMintOpen() == public_mint_open
    assert other_deed_clone.allowListMintOpen() == allow_list_mint_open
    with pytest.raises(exceptions.VirtualMachineError):
        other_deed_clone.editMintWindows(True, True, {"from": non_owner})

    return other_deed_clone, deployer_account


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
    skip_live_testing
    other_deed_clone, allowed_list = test_set_allow_list(
        get_contract, skip_live_testing
    )
    deployer_account = get_contract[1]
    allow_list_mint_open = True

    other_deed_clone.editMintWindows(
        False, allow_list_mint_open, {"from": deployer_account}
    )
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
    with pytest.raises(exceptions.VirtualMachineError):
        allow_list_mint_open = False
        other_deed_clone.editMintWindows(
            False, allow_list_mint_open, {"from": deployer_account}
        )
        other_deed_clone.allowListMint(
            {"from": account_allowed, "value": ALLOWED_LIST_PRICE}
        )


def test_public_mint(skip_live_testing, get_contract):
    # Arrange
    skip_live_testing
    other_deed_clone, deployer_account = get_contract
    public_mint_open = True
    other_deed_clone.editMintWindows(
        public_mint_open, False, {"from": deployer_account}
    )
    not_enough_value = Web3.toWei(0.0001, "ether")
    minter_account = get_account(index=1)

    # Act
    other_deed_clone.publicMint({"from": minter_account, "value": PUBLIC_PRICE})

    # Assert
    assert other_deed_clone.ownerOf(0) == minter_account
    with pytest.raises(exceptions.VirtualMachineError):
        other_deed_clone.publicMint({"from": minter_account, "value": not_enough_value})
    with pytest.raises(exceptions.VirtualMachineError):
        public_mint_open = False
        other_deed_clone.editMintWindows(
            public_mint_open, False, {"from": deployer_account}
        )
        other_deed_clone.publicMint({"from": minter_account, "value": PUBLIC_PRICE})

    return other_deed_clone, deployer_account


def test_withdraw(skip_live_testing, get_contract):
    # Arrange
    skip_live_testing
    other_deed_clone, deployer_account = test_public_mint(
        skip_live_testing, get_contract
    )
    initial_contract_balance = other_deed_clone.balance()
    receiver = deployer_account
    initial_receiver_balance = receiver.balance()
    non_owner = get_account(index=1)
    # Act
    other_deed_clone.withdraw(receiver, {"from": deployer_account})

    # Assert
    assert initial_contract_balance == PUBLIC_PRICE
    assert receiver.balance() == initial_receiver_balance + initial_contract_balance
    assert other_deed_clone.balance() == 0
    with pytest.raises(exceptions.VirtualMachineError):
        other_deed_clone.withdraw(receiver, {"from": non_owner})


def test_set_base_uri(skip_live_testing, get_contract):
    # Arrange
    skip_live_testing
    other_deed_clone, deployer_account = test_public_mint(
        skip_live_testing, get_contract
    )

    # Act
    other_deed_clone._setBaseURI(METADATA_BASE_URI, {"from": deployer_account})

    # Assert
    assert other_deed_clone.tokenURI(0) == METADATA_BASE_URI + "0" + ".json"


def test_token_uri(skip_live_testing, get_contract):
    # Arrange
    skip_live_testing
    other_deed_clone, deployer_account = test_public_mint(
        skip_live_testing, get_contract
    )
    other_deed_clone._setBaseURI(METADATA_BASE_URI, {"from": deployer_account})
    expected_token_uri = METADATA_BASE_URI + str(0) + ".json"

    # Act
    token_uri = other_deed_clone.tokenURI(0, {"from": deployer_account})

    # Assert
    assert token_uri == expected_token_uri


# TEST INTERNAL FUNCTIONS


def test_internal_mint(skip_live_testing, get_exposed_contract):
    # Arrange
    skip_live_testing
    exposed_other_deed_clone, deployer_account = get_exposed_contract
    minter_account = get_account(index=1)
    max_tokens_mint = exposed_other_deed_clone.maxSupply()
    # Act
    exposed_other_deed_clone._internalMint({"from": minter_account})

    # Assert
    assert exposed_other_deed_clone._tokenIdCounter() == 1
    with pytest.raises(exceptions.VirtualMachineError):
        for i in range(max_tokens_mint + 1):
            exposed_other_deed_clone._internalMint({"from": minter_account})
