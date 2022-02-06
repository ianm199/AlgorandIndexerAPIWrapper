import pandas as pd
from typing import List, Dict
from algo_models import AssetTransferTransaction, PaymentTransaction, AlgorandTransaction
from algo_indexer_api import User

transactions_table_cols = ['sender', 'receiver', 'confirmed_round', 'amount', 'asset_id', 'transaction_id']
db_table = pd.DataFrame(columns=transactions_table_cols)

def calculate_balance_of_account(account_id: str, df_table: str, asset_id: int) -> int:
    involves_account = df_table['sender']==account_id or df_table['receiver']==account_id
    account_rows = df_table[involves_account]
    print("test!")
    pass


def process_all_transactions_for_account(account_id: str, db_table: pd.DataFrame=db_table) -> pd.DataFrame:
    """
    Processes all transactions for an account
    :param account_id: id of the account
    :param db_table: db table to append to
    :return: db table
    """
    user = User()
    account = user.get_algorand_account_by_id(account_id)
    max_round = account.current_round
    min_round = account.get_created_at_round()
    transactions = user.get_transactions_by_account(account_id, min_round=min_round, max_round=max_round)
    tx_count = 0
    while len(transactions.transactions) != 0:
        try:
            for transaction in transactions.transactions:
                tx_count += 1
                db_table = transaction.process_transaction(db_table)
            next_token = transactions.next_token
            if not next_token:
                print(f"Exiting at round: {transaction.confirmed_round} because there is no next token")
                return db_table
            transactions = user.get_transactions_by_account(account_id, min_round=min_round, max_round=max_round, next_token=next_token)
            print(f"TX_COUNT: {tx_count} Last confirmed round {transaction.confirmed_round}")
        except Exception as e:
            print(f"excepted error {str(e)} and returned db table at {transaction.confirmed_round}")
            return db_table
    return db_table


def process_account_transactions(account_id: str, db_table: pd.DataFrame=db_table, limit=1000) -> pd.DataFrame:
    """
    Will process the transactions for all the transactions for the account
    :param account_id: str algorand account id
    :param db_table: pandas table to use, hardcoded for now
    :return: dataframe with all the transaction data processed
    """
    user = User()
    account = user.get_algorand_account_by_id(account_id)
    max_round = account.current_round
    min_round = account.get_created_at_round()
    transactions = user.get_transactions_by_account(account_id, min_round=min_round, max_round=max_round)
    for transaction in transactions.transactions:
        db_table = transaction.process_transaction(db_table)
    return db_table


def process_transactions(transactions: List[AlgorandTransaction], db_table: pd.DataFrame=db_table) -> pd.DataFrame:
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


if __name__ == '__main__':
    ALGO_MAINNET_CONTRACT = "TY5N6G67JWHSMWFFFZ252FXWKLRO5UZLBEJ4LGV7TPR5PVSKPLDWH3YRXU"
    USDC_MAINNET_CONTRACT = "ABQHZLNGGPWWZVA5SOQO3HBEECVJSE3OHYLKACOTC7TC4BS52ZHREPF7QY"
    new_df = process_all_transactions_for_account(USDC_MAINNET_CONTRACT)
    new_df.to_csv("USDC_MAINNET_CONTRACT.csv")
    df = pd.read_csv("USDC_MAINNET_CONTRACT.csv")
    senders = df.loc[df['sender']==USDC_MAINNET_CONTRACT]
    receivers = df.loc[df['receiver']==USDC_MAINNET_CONTRACT]
    max_block = max(df['confirmed_round'])
    sum_received = sum(list(receivers['amount']))
    sum_sent = sum(list(senders['amount']))
    total_algos = (sum_received - sum_sent) / 1000000
    calculate_balance_of_account(ALGO_MAINNET_CONTRACT, df, 0)