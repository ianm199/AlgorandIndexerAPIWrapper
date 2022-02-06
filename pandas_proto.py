import pandas as pd
from dataclasses import dataclass, field
from typing import List, Dict
import requests


class Transaction:
    ASSETS_WE_CARE_ABOUT = {"465865291": "STBL",
                            "386195940": "goETH",
                            "386192725": "goBTC",
                            "31566704": "USDC",
                            "465818547": "ALGO"}

    def get_asset_id(self) -> int:
        raise NotImplementedError

    def valid_asset(self) -> bool:
        return str(self.get_asset_id()) in Transaction.ASSETS_WE_CARE_ABOUT.keys()

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
class PaymentTransaction(Transaction):
    amount: int = field(default_factory=int)
    close_amount: int = field(default_factory=int)
    close_remainder_to: str = field(default_factory=str)
    receiver: str = field(default_factory=str)
    id: int = field(default_factory=int)
    confirmed_round: int = field(default_factory=int)


    def get_asset_id(self) -> int:
        return 0


@dataclass
class AssetTransferTransaction(Transaction):
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



CONTRACT_ADDRESS_DICT = {"TY5N6G67JWHSMWFFFZ252FXWKLRO5UZLBEJ4LGV7TPR5PVSKPLDWH3YRXU": "ALGO",
                         "ABQHZLNGGPWWZVA5SOQO3HBEECVJSE3OHYLKACOTC7TC4BS52ZHREPF7QY": "USDC",
                         "W5UCMHDSTGKWBOV6YVLDVPJGPE4L4ISTU6TGXC7WRF63Y7GOVFOBUNJB5Q": "goBTC",
                         "KATD43XBJJIDXB3U5UCPIFUDU3CZ3YQNVWA5PDDMZVGKSR4E3QWPJX67CY": "goETH",
                         "OPY7XNB5LVMECF3PHJGQV2U33LZPM5FBUXA3JJPHANAG5B7GEYUPZJVYRE": "STBL"}

transactions_table_cols = ['sender', 'receiver', 'confirmed_round', 'amount', 'asset_id', 'transaction_id']
db_table = pd.DataFrame(columns=transactions_table_cols)



def process_transactions(transactions: List, db_table: pd.DataFrame=db_table) -> pd.DataFrame:
    for transaction in transactions:
        id = transaction['id']
        confimed_round = transaction['confirmed-round']
        inner_transaction = False
        if 'asset-transfer-transaction' in transaction:
            trans = AssetTransferTransaction.init_from_json(transaction['asset-transfer-transaction'], id = id, confirmed_round = confimed_round)
            trans.sender = transaction['sender']
        elif 'application-transaction' in transaction:
            application_transaction = transaction
            if 'inner-txns' in application_transaction:
                inner_txns: List[dict] = application_transaction['inner-txns']
                for txn in inner_txns:
                    if txn['tx-type'] == 'pay':
                        trans = PaymentTransaction.init_from_json(txn['payment-transaction'], id = id, confirmed_round = confimed_round)
                        trans.sender = txn['sender']
                        inner_transaction = True
                    elif txn['tx-type'] == 'axfer':
                        trans = AssetTransferTransaction.init_from_json(txn['asset-transfer-transaction'], id = id, confirmed_round = confimed_round)
                        trans.sender = txn['sender']
                        inner_transaction = True
            else:
                continue
        else:
            continue
        if not trans.valid_asset():
            continue
        sender = trans.sender
        if inner_transaction:
            sender = trans.receiver
            receiver = trans.sender
        id = trans.id
        confirmed_round = trans.confirmed_round
        new_data = [sender, receiver, confirmed_round, trans.amount, trans.asset_id, id]
        new_df = pd.DataFrame(columns=transactions_table_cols, data=[new_data])
        db_table = db_table.append(new_df)
    return db_table


def get_algorand_block_transaction(block_number: int):
    base_url =f"https://algoindexer.algoexplorerapi.io/v2/blocks/{block_number}"
    req = requests.request("GET", base_url).json()
    return req['transactions']

if __name__ == '__main__':
    transactions = get_algorand_block_transaction(18920083)
    df = process_transactions(transactions)
    print("Test!")
    pt = PaymentTransaction.init_from_json({"amount":10, "receiver":10, "close_amount":10, "close_remainder_to":10})
    print("Test!")