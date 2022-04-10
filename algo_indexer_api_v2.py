import requests
from models.algorand_block import AlgorandBlock
from models.algorand_transaction import AlgorandTransaction
from models.request_models import AlgorandTransactionsReq
from models.algorand_application import AlgorandApplication
from models.algorand_asset import AlgorandAsset
from models.algorand_account import AlgorandAccount
from models.account_balances import AccountBalanceReq
import urllib

class APIUser:
    """
    Class to allow a User to easily interact with the AlgorandIndexer API in a fully typed manner. Based on docs from
    https://algoexplorer.io/api-dev/indexer-v2
    """
    BASE_URL = "https://algoindexer.algoexplorerapi.io/v2/"

    def get_algorand_block(self, block_number: int) -> AlgorandBlock:
        """
        Gets an Algorand Block by round #
        :param block_number: the block/ round # to get
        :return: AlgorandBlock object representing the requested block
        """
        full_url = self.BASE_URL + f"blocks/{block_number}"
        block = requests.get(full_url).json()
        return AlgorandBlock.init_from_json_dict(block)

    def get_algorand_transaction(self, transaction_id: str) -> AlgorandTransaction:
        """
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
        full_url = self.BASE_URL + f"/accounts/{account_id}/transactions?limit={limit}"
        if kwargs:
            params_string = self.create_params_string_from_kwargs(kwargs)
            full_url += f"&{params_string}"
        account_transactions = requests.get(full_url).json()
        return AlgorandTransactionsReq.init_from_json_dict(account_transactions)

    def get_algorand_application(self, application_id: int) -> AlgorandApplication:
        full_url = self.BASE_URL + f"/applications/{application_id}"
        application = requests.get(full_url).json()
        return AlgorandApplication.init_from_json_dict(application)

    def get_asset(self, asset_id: int) -> AlgorandAsset:
        full_url = self.BASE_URL + f"/assets/{asset_id}"
        asset = requests.get(full_url).json()
        return AlgorandAsset.init_from_json_dict(asset)

    def get_account(self, account_id: str, **kwargs) -> AlgorandAccount:
        """
        Get an algorand account object by ID
        """
        full_url = self.BASE_URL + f"/accounts/{account_id}"
        account = requests.get(full_url).json()
        return AlgorandAccount.init_from_json_dict(account)

    def get_asset_balances(self, asset_id: str, limit: int =100, **kwargs) -> AccountBalanceReq:
        """
        Get the balances in accounts for an asset
        """
        full_url = self.BASE_URL + f"/assets/{asset_id}/balances?limit={limit}"
        if kwargs:
            params_string = self.create_params_string_from_kwargs(kwargs)
            full_url += f"&{params_string}"
        balances = requests.get(full_url).json()
        return AccountBalanceReq.init_from_json_dict(balances)


    @staticmethod
    def create_params_string_from_kwargs(kwargs_dict: dict) -> str:
        full_params_dict = {}
        for key, item in kwargs_dict.items():
            key = key.replace("_", "-")
            full_params_dict[key] = item
        params_string = urllib.parse.urlencode(full_params_dict)
        return params_string


