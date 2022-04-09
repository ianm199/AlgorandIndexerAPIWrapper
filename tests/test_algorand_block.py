from models.algorand_block import AlgorandBlock
from unittest import TestCase
from algo_indexer_api_v2 import APIUser

class TestAlgoBlock(TestCase):

    def test_init(self):
        """
        Just tests that a block can be fetched properly
        """
        block_number = 18931547
        block = APIUser().get_algorand_block(block_number)
        self.assertEqual(block.round, block_number)
        self.assertEqual(len(block.transactions), 180)
        self.assertEqual(block.genesis_id, 'mainnet-v1.0')

