import os
from dotenv import dotenv_values
from algosdk import mnemonic, account
from algofi.v1.client import AlgofiTestnetClient, AlgofiMainnetClient
from algofi.v1.mint import TransactionGroup
from algofi.utils import get_ordered_symbols, prepare_payment_transaction, get_new_account

# from example_utils import print_market_state, print_user_state, print_staking_contract_state
# load user passphrase
my_path = os.path.abspath(os.path.dirname(__file__))
ENV_PATH = os.path.join(my_path, ".env")
user = dotenv_values(ENV_PATH)
sender = mnemonic.to_public_key(user['mnemonic'])
key =  mnemonic.to_private_key(user['mnemonic'])
# IS_MAINNET
IS_MAINNET = False
client = AlgofiMainnetClient(user_address=sender) if IS_MAINNET else AlgofiTestnetClient(user_address=sender)

ALGO, USDC, goBTC, goETH, STBL = "ALGO", "USDC", "goBTC", "goETH", "STBL"

class AlgoUser:

    def __init__(self, mnemoic_str: str, test_net: bool = True):
        self.public_key = mnemonic.to_public_key(mnemoic_str)
        self.private_key = mnemonic.to_private_key(mnemoic_str)
        self.client = AlgofiTestnetClient(user_address=self.public_key) if test_net else AlgofiMainnetClient(user_address=self.public_key)

    @classmethod
    def init_from_env(cls, test_net: bool = True):
        my_path = os.path.abspath(os.path.dirname(__file__))
        ENV_PATH = os.path.join(my_path, ".env")
        user = dotenv_values(ENV_PATH)
        mnemonic_phrase = user['mnemonic']
        return AlgoUser(mnemonic_phrase, test_net=test_net)

    def sign_and_submit(self, transaction: TransactionGroup, wait: bool = True) -> None:
        transaction.sign_with_private_key(self.public_key, self.private_key)
        transaction.submit(self.client.algod, wait=wait)

    def supply_asset(self, symbol: str, amount: int) -> None:
        # This turns your algo into bAlgo, what I think is a wrapped form of algo from AlgoFi under the hood
        bank_transaction: TransactionGroup = client.prepare_mint_transactions(symbol, amount, sender)
        # self.sign_and_submit(bank_transaction)
        bank_asset_balance = client.get_user_balance(self.client.get_market(ALGO).get_asset().get_bank_asset_id())
        # print(f"Bank asset balance: {bank_asset_balance} user asset balance: {}")
        # Now we want to add the bAlgo as collateral
        # collateral_transaction: TransactionGroup = self.client.prepare_add_collateral_transactions(symbol, amount, self.public_key)
        # self.sign_and_submit(collateral_transaction)

    def remove_collateral(self, symbol: str, amount: int) -> None:
        remove_collateral: TransactionGroup = self.client.prepare_remove_collateral_transactions(symbol, amount, self.public_key)
        self.sign_and_submit(remove_collateral)

    def stake_asset(self, staking_contract_name: str, amount: int):
        staking_transaction: TransactionGroup = self.client.prepare_stake_transactions(staking_contract_name, amount, self.public_key)
        self.sign_and_submit(staking_transaction)

    def borrow_asset(self, symbol: str, amount: int) -> None:
        borrow_transaction: TransactionGroup = self.client.prepare_borrow_transactions(symbol, amount, self.public_key)
        self.sign_and_submit(borrow_transaction)

    def borrow_and_stake(self, symbol: str, amount: int):
        self.borrow_asset(symbol, amount)
        self.stake_asset(symbol, amount)


    def print_asset_state(self, symbol: str):
        print(f"Bank balance {self.get_bank_balance(symbol)} \nUser balance: {self.get_user_balance(symbol)}")

    def get_bank_balance(self, symbol: str):
        return client.get_user_balance(client.get_market(symbol).get_asset().get_bank_asset_id())

    def get_user_balance(self, symbol: str):
        return client.get_user_balance(client.get_market(symbol).get_asset().get_underlying_asset_id())

class Utils:

    def __init__(self, mnemoic_str: str, test_net: bool = True):
        self.public_key = mnemonic.to_public_key(mnemoic_str)
        self.private_key = mnemonic.to_private_key(mnemoic_str)
        self.client = AlgofiTestnetClient(user_address=self.public_key) if test_net else AlgofiMainnetClient(user_address=self.public_key)

    @classmethod
    def init_from_env(cls, test_net: bool = True):
        my_path = os.path.abspath(os.path.dirname(__file__))
        ENV_PATH = os.path.join(my_path, ".env")
        user = dotenv_values(ENV_PATH)
        mnemonic_phrase = user['mnemonic']
        return Utils(mnemonic_phrase, test_net=test_net)

    def get_asset_id(self, symbol: str) -> int:
        return self.client.get_market(symbol).get_asset().get_bank_asse


def get_bank_balance(symbol: str=ALGO) -> int:
    symbols = client.get_active_ordered_symbols()
    if symbol not in symbols:
        raise ValueError(f"Provided symbol {symbol} not in allowed values: {symbols}")
    return client.get_user_balance(client.get_market(symbol).get_asset().get_bank_asset_id())

def get_user_balance(symbol: str=ALGO) -> int:
    return client.get_user_balance(client.get_market(symbol).get_asset().get_underlying_asset_id())


if __name__ == '__main__':
    user = AlgoUser.init_from_env(test_net=False)
    # user.print_asset_state(ALGO)
    utils: Utils = Utils.init_from_env(test_net=False)
    print(utils.get_asset_id(ALGO))