from dataclasses import dataclass, field
from typing import List, Dict
import algofi.contract_strings as contract_strings
import pandas as pd

ASSET_TRANSFER_TRANSACTION = 'asset-transfer-transaction'
APPLICATION_TRANSACTION = "application-transaction"
PAYMENT_TRANSACTION = "payment-transaction"
TRANSACTION = "transaction"
class BaseDataClass:

    @classmethod
    def init_from_json(cls, json_dict: dict):
        new_dict = convert_keys_to_snake_case(json_dict)
        return cls(**new_dict)

@dataclass
class Account(BaseDataClass):
    address: str = field(default_factory=str)
    amount: int = field(default_factory=int)
    amount_without_pending_rewards: int = field(default_factory=int)
    assets: List[Dict] = field(default_factory=list)
    created_at_round: int = field(default_factory=int)
    deleted: bool = field(default_factory=bool)
    pending_rewards: int = field(default_factory=int)
    reward_base: int = field(default_factory=int)
    rewards: int = field(default_factory=int)
    round: int = field(default_factory=int)
    status: str = field(default_factory=str)

@dataclass
class AlgorandAccount(BaseDataClass):
    account: Account
    current_round: int = field(default_factory=int)

    @classmethod
    def init_from_json(cls, json_dict: dict):
        new_dict = convert_keys_to_snake_case(json_dict['account'])
        account = Account.init_from_json(new_dict)
        return AlgorandAccount(current_round=json_dict['current-round'], account=account)

    def get_created_at_round(self) -> int:
        return self.account.created_at_round


class BaseTransactionType:
    ASSETS_WE_CARE_ABOUT = {"465865291": "STBL",
                            "386195940": "goETH",
                            "386192725": "goBTC",
                            "31566704": "USDC",
                            "0": "ALGO"}

    def get_asset_id(self) -> int:
        raise NotImplementedError

    def valid_asset(self) -> bool:
        return str(self.get_asset_id()) in BaseTransactionType.ASSETS_WE_CARE_ABOUT.keys()

    @classmethod
    def init_from_json(cls, json_dict: dict, id: int = None, confirmed_round: int = None):
        new_dict = {}
        for item in json_dict:
            new_dict[item.replace("-", "_")] = json_dict[item]
        if id:
            new_dict['id'] = id
        if confirmed_round:
            new_dict['confirmed_round'] = confirmed_round
        return cls(**new_dict)

@dataclass
class PaymentTransaction(BaseTransactionType):
    amount: int = field(default_factory=int)
    close_amount: int = field(default_factory=int)
    close_remainder_to: str = field(default_factory=str)
    receiver: str = field(default_factory=str)
    id: int = field(default_factory=int)
    confirmed_round: int = field(default_factory=int)


    def get_asset_id(self) -> int:
        return 0


@dataclass
class AssetTransferTransaction(BaseTransactionType):
    amount: int = field(default_factory=int)
    asset_id: int = field(default_factory=int)
    close_amount: int = field(default_factory=int)
    close_to: str = field(default_factory=str)
    receiver: str = field(default_factory=str)
    sender: str = field(default_factory=str)
    id: int = field(default_factory=int)
    confirmed_round: int = field(default_factory=int)


    def get_asset_id(self) -> int:
        return self.asset_id

@dataclass
class Signature:
    sig: str = field(default_factory=str)

@dataclass
class AlgorandTransaction:
    transaction: dict
    transaction_type: str
    signature: Signature
    close_rewards: int = field(default_factory=int)
    closing_amount: int = field(default_factory=int)
    confirmed_round: int = field(default_factory=int)
    fee: int = field(default_factory=int)
    first_valid: int = field(default_factory=int)
    genesis_hash: str = field(default_factory=str)
    genesis_id: str = field(default_factory=str)
    global_state_delta: List[Dict] = field(default_factory=list)
    group: str = field(default_factory=str)
    id: str = field(default_factory=str)
    inner_txns: List[Dict] = field(default_factory=list)
    intra_round_offset: int = field(default_factory=int)
    last_valid: int = field(default_factory=int)
    local_state_delta: List[Dict] = field(default_factory=list)
    note: str = field(default_factory=str)
    receiver_rewards: int = field(default_factory=int)
    round_time: int = field(default_factory=int)
    sender: str = field(default_factory=str)
    sender_rewards: int = field(default_factory=int)
    tx_type: str = field(default_factory=str)

    def is_asset_transfer(self) -> bool:
        return self.transaction_type == ASSET_TRANSFER_TRANSACTION

    def is_application_transaction(self) -> bool:
        return self.transaction_type == APPLICATION_TRANSACTION

    def is_payment_transaction(self):
        return self.transaction_type == PAYMENT_TRANSACTION

    @classmethod
    def init_from_json_dict(cls, json_dict: dict):
        new_dict = convert_keys_to_snake_case(json_dict)
        if ASSET_TRANSFER_TRANSACTION in json_dict or ASSET_TRANSFER_TRANSACTION.replace("-", "_") in json_dict:
            new_dict['transaction'] = new_dict[ASSET_TRANSFER_TRANSACTION.replace("-", "_")]
            new_dict['transaction_type'] = ASSET_TRANSFER_TRANSACTION
            del new_dict[ASSET_TRANSFER_TRANSACTION.replace("-", "_")]
        elif APPLICATION_TRANSACTION in json_dict or APPLICATION_TRANSACTION.replace("-", "_") in json_dict:
            new_dict['transaction'] = new_dict[APPLICATION_TRANSACTION.replace("-", "_")]
            new_dict['transaction_type'] = APPLICATION_TRANSACTION
            del new_dict[APPLICATION_TRANSACTION.replace("-", "_")]
        elif PAYMENT_TRANSACTION in json_dict or PAYMENT_TRANSACTION.replace("-", "_") in json_dict:
            new_dict['transaction'] = new_dict[PAYMENT_TRANSACTION.replace("-", "_")]
            new_dict['transaction_type'] = PAYMENT_TRANSACTION
            del new_dict[PAYMENT_TRANSACTION.replace("-", "_")]
        else:
            raise ValueError(f"Unsupported tx type: {json_dict}")
        return AlgorandTransaction(**new_dict)

    def process_transaction(self, db_table: pd.DataFrame) -> pd.DataFrame:
        """
        This function processed a transaction, by grabbing the raw transaction data from the larger transaction and puts
        it into a dataframe. It stores: ['sender', 'receiver', 'confirmed_round', 'amount', 'asset_id', 'transaction_id']
        so that we can process the raw data data into user account summaries
        :param db_table: tabel with cols ['sender', 'receiver', 'confirmed_round', 'amount', 'asset_id', 'transaction_id']
        :return: updated dataframe
        """
        is_inner_transaction = False
        if self.is_asset_transfer():
            trans = AssetTransferTransaction.init_from_json(self.transaction)
            trans.sender = self.sender
        elif self.is_payment_transaction():
            self.transaction['id'] = self.id
            self.transaction['confirmed_round'] = self.confirmed_round
            trans = PaymentTransaction.init_from_json(self.transaction)
            trans.sender = self.sender
        elif self.is_application_transaction():
            if self.inner_txns:
                for innner_txn in self.inner_txns:
                    if innner_txn['tx-type'] == "pay":
                        trans = PaymentTransaction.init_from_json(innner_txn['payment-transaction'])
                        trans.sender = innner_txn['sender']
                        trans.id = self.id
                        trans.confirmed_round = self.confirmed_round
                    elif innner_txn['tx-type'] == "axfer":
                        trans = AssetTransferTransaction.init_from_json(innner_txn['asset-transfer-transaction'])
                        trans.sender = innner_txn['sender']
                        trans.id = self.id
                        trans.confirmed_round = self.confirmed_round
            else:
                print("No valid transaction, returning un-updated DF")
                return db_table
        if not trans.valid_asset():
            print(f"Invalid asset_id {trans.get_asset_id()}, returning db without update")
            return db_table
        sender = trans.sender
        receiver = trans.receiver
        id = trans.id
        confirmed_round = trans.confirmed_round
        new_data = [sender, receiver, confirmed_round, trans.amount, trans.get_asset_id(), id]
        new_df = pd.DataFrame(columns=db_table.columns, data=[new_data])
        full_df = pd.concat([db_table, new_df])
        return full_df



@dataclass
class AlgorandTransactionReq:
    current_round: int
    transaction: AlgorandTransaction

    @classmethod
    def init_from_json_dict(cls, json_dict: dict):
        new_dict = convert_keys_to_snake_case(json_dict)
        new_dict[TRANSACTION] = AlgorandTransaction.init_from_json_dict(json_dict[TRANSACTION])
        return AlgorandTransactionReq(**new_dict)

@dataclass
class AlgorandTransactionsReq:
    current_round: int
    transactions: List[AlgorandTransaction]
    next_token: str = field(default_factory=str)

    @classmethod
    def init_from_json_dict(cls, json_dict: dict):
        new_dict = convert_keys_to_snake_case(json_dict)
        json_dict['transactions'] = list(map(lambda trans: convert_keys_to_snake_case(trans), json_dict['transactions']))
        new_dict['transactions'] = list(map(lambda trans: AlgorandTransaction.init_from_json_dict(trans), json_dict['transactions']))
        return AlgorandTransactionsReq(**new_dict)

@dataclass
class Transactions:
    transactions: List[AlgorandTransaction]
    current_round: int = field(default_factory=int)
    next_token: str = field(default_factory=str)

@dataclass
class Rewards:
    fee_sink: str = field(default_factory=str)
    rewards_calculation_round: int = field(default_factory=int)
    rewards_level: int = field(default_factory=int)
    rewards_pool: str = field(default_factory=str)
    rewards_rate: int = field(default_factory=int)
    rewards_residue: int = field(default_factory=int)

@dataclass
class AlgorandBlock:
    transactions: List[AlgorandTransaction]
    rewards: Rewards
    genesis_hash: str = field(default_factory=str)
    genesis_id: str = field(default_factory=str)
    previous_block_hash: str = field(default_factory=str)
    round: int = field(default_factory=int)
    seed: str = field(default_factory=str)
    timestamp: int = field(default_factory=int)
    transactions_root: str = field(default_factory=str)
    txn_counter: int = field(default_factory=int)
    upgrade_state: dict = field(default_factory=dict)
    upgrade_vote: dict = field(default_factory=dict)

    @classmethod
    def init_from_json(cls, json_dict: dict):
        new_dict = convert_keys_to_snake_case(json_dict)
        new_dict['transactions'] = list(map(lambda trans: AlgorandTransaction.init_from_json_dict(trans), new_dict['transactions']))
        new_dict['rewards'] = convert_keys_to_snake_case(new_dict['rewards'])
        return AlgorandBlock(**new_dict)

    def get_transactions_by_account(self, account_id: str) -> List[AlgorandTransaction]:
        result = []
        for transaction in self.transactions:
            if transaction.sender == account_id or transaction.transaction_type == ASSET_TRANSFER_TRANSACTION and transaction.transaction['receiver'] == account_id:
                result.append(transaction)
        return result


def convert_keys_to_snake_case(dict_to_fix: dict) -> dict:
    result = {}
    for key, value in dict_to_fix.items():
        new_key = key.replace("-", "_")
        result[new_key] = value
    return result