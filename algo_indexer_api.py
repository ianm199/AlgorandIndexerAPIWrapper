import pprint

import requests
from algo_models import AlgorandAccount, AlgorandTransactionReq, AlgorandTransactionsReq, AlgorandBlock

def process_transactions_for_account(account_number: int):
    pass


class User:
    CONTRACT_ADDRESS_DICT = {"ALGO": "TY5N6G67JWHSMWFFFZ252FXWKLRO5UZLBEJ4LGV7TPR5PVSKPLDWH3YRXU",
                             "USDC": "ABQHZLNGGPWWZVA5SOQO3HBEECVJSE3OHYLKACOTC7TC4BS52ZHREPF7QY",
                             "goBTC": "W5UCMHDSTGKWBOV6YVLDVPJGPE4L4ISTU6TGXC7WRF63Y7GOVFOBUNJB5Q",
                             "goETH": "KATD43XBJJIDXB3U5UCPIFUDU3CZ3YQNVWA5PDDMZVGKSR4E3QWPJX67CY",
                             "STBL": "OPY7XNB5LVMECF3PHJGQV2U33LZPM5FBUXA3JJPHANAG5B7GEYUPZJVYRE"}
    BASE_URL = "https://algoindexer.algoexplorerapi.io/v2/"

    def get_transactions_by_account(self, account_id: str, max_round: int, min_round: int, next_token = None) -> AlgorandTransactionsReq:
        full_url = User.BASE_URL + f"accounts/{account_id}/transactions?limit=100&max-round={max_round}&min-round={min_round}"
        if next_token:
            full_url += f"&next={next_token}"
        transactions = requests.get(full_url).json()
        return AlgorandTransactionsReq.init_from_json_dict(transactions)

    def get_algorand_account_by_id(self, account_id: str) -> AlgorandAccount:
        full_url = User.BASE_URL + f"accounts/{account_id}"
        account_info = requests.get(full_url).json()
        return AlgorandAccount.init_from_json(account_info)

    def get_transaction_by_id(self, tx_id: str) -> AlgorandTransactionReq:
        full_url = User.BASE_URL + f"transactions/{tx_id}"
        transaction = requests.get(full_url).json()
        return AlgorandTransactionReq.init_from_json_dict(transaction)

    def get_algorand_block(self, block_number: int) -> AlgorandBlock:
        full_url = User.BASE_URL + f"blocks/{block_number}"
        block = requests.get(full_url).json()
        return AlgorandBlock.init_from_json(block)




if __name__ == '__main__':
    block_number = 18931547
    account_id = "TY5N6G67JWHSMWFFFZ252FXWKLRO5UZLBEJ4LGV7TPR5PVSKPLDWH3YRXU"
    block = User().get_algorand_block(block_number)
    # algo_account = User().get_algorand_account_by_id(account_id)
    # print(algo_account.get_created_at_round())
    pprint.pprint(block.transactions[152].__dict__)
    for i, transaction in enumerate(block.transactions):
        print(i, transaction.transaction_type)
    print("test!")