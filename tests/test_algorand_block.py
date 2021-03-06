import pprint
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
        self.assertEqual(block.rewards.fee_sink, 'Y76M3MSY6DKBRHBL7C3NNDXGS5IIMQVQVUAB6MP4XEMMGVF2QWNPL226CA')
        # self.assertEqual(block.transactions[0].payment_transaction.receiver, 'LPYK3QS5DLIT7BTGAOKM5ALYUJEKQVFMUNPKG6AJ6QD2W6CLS3XEZQSEJI')

    def test_other_block(self):
        block_number = 20335116
        block = APIUser().get_algorand_block(block_number)
        self.assertEqual(block.round, block_number)

class TestAlgorandTransaction(TestCase):

    def test_asset_transfer_get(self):
        """
        Testing API can read random transaction found on algo explorer
        """
        transaction_id = "PTL5XNFA2DLUFNUC5RBD2OHS4HFUOTUOT5A3NEQYXETKMT2BXEUA"
        transaction = APIUser().get_algorand_transaction(transaction_id)
        self.assertEqual(transaction.tx_type, "axfer")
        self.assertEqual(transaction.sender, "C7RYOGEWDT7HZM3HKPSMU7QGWTRWR3EPOQTJ2OHXGYLARD3X62DNWELS34")
        self.assertEqual(transaction.asset_transfer_transaction.asset_id, 127746157)

    def test_app_call(self):
        transaction_id = "PRYG5NCMHKJ67YED7PPBRRIN5IH4BMFSW6EDXFY4J7SAJDXMZUZQ"
        transaction = APIUser().get_algorand_transaction(transaction_id)
        self.assertEqual(transaction.id, transaction_id)

    def test_application_call_get(self):
        """
        testing API can read deeply nested application call transactions properly
        """
        transaction_id = "NICW4RQD2IY76Q6MLO5DWFJM66SHXW2NJCU6HTQZXPFQZ7QC2DEQ"
        transaction = APIUser().get_algorand_transaction(transaction_id)
        self.assertEqual(transaction.application_transaction.application_args, ["ZHVtbXlfZWlnaHQ="])

    def test_payment_transaction_get(self):
        """
        testing API can read payment transactions
        """
        transaction_id = "E5ZBBET55LZLTOFLVHVLM3VZFQ3XERAT7QDAIZ4ODMIGLXJILSTQ"
        transaction = APIUser().get_algorand_transaction(transaction_id)
        self.assertEqual(transaction.payment_transaction.receiver, "NHHLK67CYONVDXT4H5LNXDHDB6B453P2BDPLEZJ3ZBHKVO3AP3L5V4WQL4")
        self.assertEqual(transaction.id, transaction_id)

    def test_state_delta_changes_get(self):
        """
        testing API can read the state delta correctly

        TODO: Can use this as an example of how to improve after this iteration. The local state delta code not fully covered
        """
        transaction_id = "Y5EGI4TVGFMEQDGPTRBAOZNE6XSIZREWET3DGGHTQ5YXGEVPP7NA"
        transaction = APIUser().get_algorand_transaction(transaction_id)
        self.assertEqual(transaction.local_state_delta[0].delta[0]['key'],'bwAAAAAB4atw')

class TestTransactions(TestCase):

    def test_get_account_transactions(self):
        """
        Tests that API can get transactions by account
        """
        account_id = "FPOU46NBKTWUZCNMNQNXRWNW3SMPOOK4ZJIN5WSILCWP662ANJLTXVRUKA"
        transactions = APIUser().get_account_transactions(account_id=account_id)
        self.assertEqual(len(transactions.transactions), 100)

    def test_get_transactions_nested(self):
        tx_id = "YHVV7ANVCAPYLLYYKGJTO7NDQY73BXLKPQENUIBBDGKW6NX4YXGA"
        account_id = "FPOU46NBKTWUZCNMNQNXRWNW3SMPOOK4ZJIN5WSILCWP662ANJLTXVRUKA"
        transactions = APIUser().get_account_transactions(account_id=account_id, txid=tx_id, max_round=20327413)
        self.assertEqual(transactions.transactions[0].asset_transfer_transaction.asset_id, 31566704)

    def test_get_asset_transactions(self):
        usdc_id = 31566704
        transactions = APIUser().get_asset_transactions(asset_id=usdc_id)
        self.assertEqual(len(transactions.transactions), 100)

class TestAlgorandApplication(TestCase):
    """
    Tests for the AlgorandApplication classes/ routes
    """

    def test_get_algorand_application(self):
        """
        Testing one of the mainnet contracts for Algofi
        https://algoexplorer.io/application/465814065
        """

        application_id = 465814065
        application = APIUser().get_algorand_application(application_id=application_id)
        self.assertEqual(application.application.id, application_id)
        self.assertEqual(application.application.created_at_round, 18011216)

class TestAlgorandAsset(TestCase):
    """
    Tests for AlgorandAsset classes/ routes
    """

    def test_usdc(self):
        """
        Testing USDC asset
        https://algoexplorer.io/asset/31566704
        """
        asset_id = 31566704
        asset = APIUser().get_asset(asset_id=asset_id)
        self.assertEqual(asset.asset.created_at_round, 8874561)
        self.assertEqual(asset.asset.params.name, "USDC")

class TestAlgorandAccount(TestCase):
    """
    Tests for alogrand acconts classes/ routes
    """
    def test_get_account(self):
        account_id = "2SGUKZCOBEVGN3HPKSXPS6DTCXZ7LSP6G3BQF6KVUIUREBBY2QTGSON7WQ"
        account = APIUser().get_account(account_id=account_id)
        self.assertEqual(account.account.address, account_id)
        self.assertEqual(account.account.created_at_round, 18011267)



