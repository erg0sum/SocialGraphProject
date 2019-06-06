import pytest


@pytest.fixture
def friend_contract(w3, get_contract):
    with open('contract.vy') as f:
        contract_code = f.read()
        contract = get_contract(contract_code)
    return contract

def test_initial_state(w3, tester, friend_contract):
    k1, k2, k3, k4, k5 = w3.eth.accounts[:5]

    # Check beneficiary is correct
    assert friend_contract is not None
    assert friend_contract.listFriends(k1) == [None] * 256

def test_add_friend(w3, tester, friend_contract, get_logs):
    k1, k2, k3, k4, k5 = w3.eth.accounts[:5]
    tx_hash = friend_contract.addFriend(k2, transact={'from':k3})
    w3.testing.mine(1)

    log = get_logs(tx_hash, friend_contract, "AddFriend")
    assert log[0]["args"]["friend"] == k2
    assert log[0]["args"]["sender"] == k3
    
    k3_friends = friend_contract.listFriends(k3)
    assert k3_friends[0] == k2

def test_double_add_friend(w3, tester, friend_contract, get_logs):
    k1, k2, k3, k4, k5 = w3.eth.accounts[:5]
    tx_hash = friend_contract.addFriend(k2, transact={'from':k3})
    w3.testing.mine(1)

    tx_hash = friend_contract.addFriend(k2, transact={'from':k3})
    w3.testing.mine(1)

    log = get_logs(tx_hash, friend_contract, "AddFriend")
    assert len(log) == 0
    
    k3_friends = friend_contract.listFriends(k3)
    assert k3_friends[0] == k2
    assert k3_friends[1] == None
    assert friend_contract.countFriends(k3) == 1