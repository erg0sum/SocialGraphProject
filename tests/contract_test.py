from vyper import compiler
from web3 import Web3
from eth_tester import (
    EthereumTester,
)
from web3.providers.eth_tester import (
    EthereumTesterProvider,
)
from eth_tester.exceptions import (
    TransactionFailed,
)

t = EthereumTester()

def w3(tester):
    def zero_gas_price_strategy(web3, transaction_params=None):
        return 0  # zero gas price makes testing simpler.

    w3 = Web3(EthereumTesterProvider(tester))
    w3.eth.setGasPriceStrategy(zero_gas_price_strategy)
    return w3

def get_contract(w3, source_code, *args, **kwargs):
    out = compiler.compile_code(
        source_code,
        ['abi', 'bytecode'],
        interface_codes=kwargs.pop('interface_codes', None),
    )
    abi = out['abi']
    bytecode = out['bytecode']
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    value = kwargs.pop('value_in_eth', 0) * 10**18  # Handle deploying with an eth value.

    c = w3.eth.contract(abi=abi, bytecode=bytecode)
    deploy_transaction = c.constructor(*args)
    tx_info = {
        'from': w3.eth.accounts[0],
        'value': value,
        'gasPrice': 0,
    }
    tx_info.update(kwargs)
    tx_hash = deploy_transaction.transact(tx_info)
    address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
    contract = w3.eth.contract(
        address,
        abi=abi,
        bytecode=bytecode,
        ContractFactoryClass=VyperContract,
    )
    return contract

# Compile and Deploy contract to provisioned testchain
# (e.g. run __init__ method) with given args (e.g. init_args)
# from msg.sender = t.k1 (private key of address 1 in test acconuts)
# and supply 1000 wei to the contract
init_args = []

contract = get_contract(w3, )