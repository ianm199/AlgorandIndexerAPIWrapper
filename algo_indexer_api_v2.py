import requests
from models.algorand_block import AlgorandBlock

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
        return AlgorandBlock.init_from_json(block)
