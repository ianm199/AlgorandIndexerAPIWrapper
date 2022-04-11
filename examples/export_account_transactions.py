from algo_indexer_api_v2 import APIUser
import pandas as pd

def export_account_payment_transactions(account_id: str, max_to_export: int = 500, output: str = "summary.csv") -> None:
    sender, receiver, amount, tx_type, asset_id = [], [], [], [], []
    user = APIUser()
    transactions_req = user.get_account_transactions(account_id)
    counter = 0
    while (transactions_req.next_token):
        for transaction in transactions_req.transactions:
            if transaction.tx_type == "pay":
                sender.append(transaction.sender)
                receiver.append(transaction.payment_transaction.receiver)
                amount.append(transaction.payment_transaction.amount)
                tx_type.append(transaction.tx_type)
                asset_id.append(0)
            if transaction.tx_type == "axfer":
                sender.append(transaction.sender)
                receiver.append(transaction.asset_transfer_transaction.receiver)
                asset_id.append(transaction.asset_transfer_transaction.asset_id)
                amount.append(transaction.asset_transfer_transaction.amount)
                tx_type.append(transaction.tx_type)
            counter += 1
            print(counter)
        if counter >= max_to_export:
            break
    # df_cols = ["sender", "receiver", "amount", "tx_type", "asset_id"]
    df_data = {"sender": sender, "receiver": receiver, "amount": amount, "tx_type": tx_type, "asset_id": asset_id}
    df = pd.DataFrame(df_data)
    df.to_csv(open(output, "w"))

if __name__ == '__main__':
    random_account_id_from_algoexplorer = "C7RYOGEWDT7HZM3HKPSMU7QGWTRWR3EPOQTJ2OHXGYLARD3X62DNWELS34"
    export_account_payment_transactions(random_account_id_from_algoexplorer)

