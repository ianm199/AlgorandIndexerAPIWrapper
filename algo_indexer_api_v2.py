import pprint

import requests
from models.algorand_block import AlgorandBlock
from models.algorand_transaction import AlgorandTransaction
from models.request_models import AlgorandTransactionsReq
from models.algorand_application import AlgorandApplication
from models.algorand_asset import AlgorandAsset
from models.algorand_account import AlgorandAccount
from models.account_balances import AccountBalanceReq
import urllib
import fire

class APIUser:
    """
    Class to allow a User to easily interact with the AlgorandIndexer API in a fully typed manner. Based on docs from
    https://algoexplorer.io/api-dev/indexer-v2

    Note that any query params specified in the API docs as using dashes, must instead use underscores. So rather than
    min-round, we'd pass in min_round as a parameter
    """
    BASE_URL = "https://algoindexer.algoexplorerapi.io/v2/"

    def get_algorand_block(self, block_number: int) -> AlgorandBlock:
        """
        Accesses route: /v/blocks/{round-number] route

        Gets an Algorand Block by round #
        :param block_number: the block/ round # to get
        :return: AlgorandBlock object representing the requested block
        """
        full_url = self.BASE_URL + f"blocks/{block_number}"
        block = requests.get(full_url).json()
        return AlgorandBlock.init_from_json_dict(block)

    def get_algorand_transaction(self, transaction_id: str) -> AlgorandTransaction:
        """
        Accesses route: /v2/transacation{txid}
        Get an algorand transaction by id
        :param transaction_id: transaction ID
        :return: Algorand Transaction Object representing the transaction specified
        """
        full_url = self.BASE_URL + f"transactions/{transaction_id}"
        transaction = requests.get(full_url).json()['transaction']
        return AlgorandTransaction.init_from_json_dict(transaction)

    def get_account_transactions(self,
                                 account_id: str,
                                 limit=100,
                                 **kwargs) -> AlgorandTransactionsReq:
        """
        Accesses route /v2/accounts/{account_id}/transactions
        Gets transactions for an account. Can add any extra query params as kwargs. Paramas are described in the API docs
        https://algoexplorer.io/api-dev/indexer-v2
        :param account_id: str account id to find
        :param limit: int limit of how many responses to contain
        :param kwargs: Extra parameters such as min_round, max_round, currency_greater_than, etc.
        :return: AlgorandTransactionsReq object which contains a list of AlgorandTransactions related to the account
        """
        full_url = self.BASE_URL + f"/accounts/{account_id}/transactions?limit={limit}"
        if kwargs:
            params_string = self.create_params_string_from_kwargs(kwargs)
            full_url += f"&{params_string}"
        account_transactions = requests.get(full_url).json()
        return AlgorandTransactionsReq.init_from_json_dict(account_transactions)

    def get_algorand_application(self, application_id: int) -> AlgorandApplication:
        """
        Accesses route: /v2/applications/{application_id}
        Gets information on Algorand applications. Returns information on their creation, state, etc.
        :param application_id: int application id
        :return: AlgorandApplication object relating to the application ID
        """
        full_url = self.BASE_URL + f"/applications/{application_id}"
        application = requests.get(full_url).json()
        return AlgorandApplication.init_from_json_dict(application)

    def get_asset(self, asset_id: int) -> AlgorandAsset:
        """
        Accesses route: /v2/assets/{asset_id}
        :param asset_id:
        :return:
        """
        full_url = self.BASE_URL + f"/assets/{asset_id}"
        asset = requests.get(full_url).json()
        return AlgorandAsset.init_from_json_dict(asset)

    def get_account(self, account_id: str, round: int = None) -> AlgorandAccount:
        """
        Accesses route /v/2accounts/{account_id}

        Get an algorand account object by ID
        """
        full_url = self.BASE_URL + f"/accounts/{account_id}"
        if round:
            full_url += "?round="
        account = requests.get(full_url).json()
        return AlgorandAccount.init_from_json_dict(account)

    def get_asset_balances(self, asset_id: int, limit: int =100, **kwargs) -> AccountBalanceReq:
        """
        Accesses route: /v2/assets/{asset-id}/balances

        Gets the balances of accounts for a specific asset
        :param asset_id: int id of the asset
        :param limit: int # of responses lmite
        :param kwargs: additional params
        :return: List of account balances in AccountBalanceReq option
        """
        full_url = self.BASE_URL + f"/assets/{asset_id}/balances?limit={limit}"
        if kwargs:
            params_string = self.create_params_string_from_kwargs(kwargs)
            full_url += f"&{params_string}"
        balances = requests.get(full_url).json()
        return AccountBalanceReq.init_from_json_dict(balances)

    def get_asset_transactions(self, asset_id: int, limit: int = 100, **kwargs) -> AlgorandTransactionsReq:
        """
        Accesses route: /v2/assets/{asset_id}/transactions

        Gets transactions that involve a specific asset
        :param asset_id: int id of the asset
        :param limit: int # of responses
        :param kwargs: additional paramas
        :return: AlgorandTransactionsReq object that contains a list of the related transactions
        """
        full_url = self.BASE_URL + f"/assets/{asset_id}/transactions?limit={limit}"
        if kwargs:
            params_string = self.create_params_string_from_kwargs(kwargs)
            full_url += f"&{params_string}"
        transactions = requests.get(full_url).json()
        return AlgorandTransactionsReq.init_from_json_dict(transactions)

    def get_most_recent_block_number(self) -> int:
        """
        Gets the most recent block #
        :return: most recent block number
        """
        full_url = "https://algoindexer.algoexplorerapi.io/health"
        return requests.get(full_url).json()['round']


    @staticmethod
    def create_params_string_from_kwargs(kwargs_dict: dict) -> str:
        full_params_dict = {}
        for key, item in kwargs_dict.items():
            key = key.replace("_", "-")
            full_params_dict[key] = item
        params_string = urllib.parse.urlencode(full_params_dict)
        return params_string


if __name__ == "__main__":
    fire.Fire(APIUser)
