import unittest

import pandas as pd
from process_transactions import process_account_transactions
from algo_indexer_api import AlgorandAccount, User

class TestAlgorandAccount(unittest.TestCase):
    """
    Some tests for the Algorand Account Data class
    """
    pass

class TestAlgorandTransactions(unittest.TestCase):

    def test_get_transaction(self):
        application_transaction_id = "SXQRTGYPYTBEUESFNDVVMBDYVDIY4CS7MJ4PZQ7BDCN3XCWVGIZA"
        transaction = User().get_transaction_by_id(application_transaction_id)
        expected_round = 18925144
        actual_round = transaction.transaction.confirmed_round
        self.assertEqual(actual_round, expected_round)

    def test_get_transactions_by_account(self):
        min_round = 18920083
        max_round = 18920084
        account_id = "HIBUB7C574EBHZCN6Q7XVILZYLRW4BGQPPMH5MHYI4MIWVZIKKUQMDPVUM"
        transactions = User().get_transactions_by_account(account_id, min_round=min_round, max_round=max_round)
        expected_first_transaction_id = "D45P7I7CORD4PYJL5UZ5TCJN6DTOEYJ4MD3WX3SD4H24VA366YGA"
        actual = transactions.transactions[0].id
        self.assertEqual(actual, expected_first_transaction_id)

class TestAlgorandBlock(unittest.TestCase):

    def test_get_block(self):
        block_number = 18931547
        block = User().get_algorand_block(block_number)
        expected_txn_counter = 574840681
        actual_txn_counter = block.txn_counter
        self.assertEqual(actual_txn_counter, expected_txn_counter)

    def test_get_transactions_by_account(self):
        block_number = 18931547
        block = User().get_algorand_block(block_number)
        account_id = "SPMV7LSRVTDE2MU5XDQPGBBU3FYYP4WN32IM55PBRWK7SY4CDCOH6YP5JA"
        by_account = block.get_transactions_by_account(account_id)
        expcted_len = 15
        actual_len = len(by_account)
        self.assertEqual(actual_len, expcted_len)

class TestProcessor(unittest.TestCase):

    TEST_ALGO_ACCOUNT = "SPMV7LSRVTDE2MU5XDQPGBBU3FYYP4WN32IM55PBRWK7SY4CDCOH6YP5JA"
    ALGO_MAINNET_CONTRACT = "TY5N6G67JWHSMWFFFZ252FXWKLRO5UZLBEJ4LGV7TPR5PVSKPLDWH3YRXU"

    def test_process_transaction_send_algo(self):
        """
        This tests the transaction of sending some algo to the ALGO mainnet contract. Link to transaction here:
        https://algoexplorer.io/tx/B4OIINJG4YCU3QCXSK7P5EABERJL4CZHDCOL6HNE4YCDG3TH5SSQ
        """
        block_number = 18931547
        block = User().get_algorand_block(block_number)
        account_id = TestProcessor.TEST_ALGO_ACCOUNT
        by_account = block.get_transactions_by_account(account_id)
        relevant_tx = by_account[14]
        transactions_table_cols = ['sender', 'receiver', 'confirmed_round', 'amount', 'asset_id', 'transaction_id']
        db_table = pd.DataFrame(columns=transactions_table_cols)
        new_df = relevant_tx.process_transaction(db_table)
        expected_sender = TestProcessor.TEST_ALGO_ACCOUNT
        expected_receiever = TestProcessor.ALGO_MAINNET_CONTRACT
        expected_amount = 3000000
        expected_transaction_id = "B4OIINJG4YCU3QCXSK7P5EABERJL4CZHDCOL6HNE4YCDG3TH5SSQ"
        expected_asset_id = 0
        expected_round = 18931547
        expected_values = [expected_sender, expected_receiever, expected_round, expected_amount, expected_asset_id, expected_transaction_id]
        actual_values = list(new_df.iloc[0])
        self.assertEqual(actual_values, expected_values)

    def test_process_withdraw_algo_transaction(self):
        """
        Tests that data is recorded correctly when withdrawing from algofi
        This transaction I withdrew some ALGO
        https://algoexplorer.io/tx/group/Jrh6%2BwLybbx4%2FSojRBth0fl4pEz%2FXOth2eFUPPMRcYs%3D
        """
        block_number = 18933620
        block = User().get_algorand_block(block_number)
        account_id = TestProcessor.TEST_ALGO_ACCOUNT
        by_account = block.get_transactions_by_account(account_id)
        relevant_tx = by_account[14]
        transactions_table_cols = ['sender', 'receiver', 'confirmed_round', 'amount', 'asset_id', 'transaction_id']
        db_table = pd.DataFrame(columns=transactions_table_cols)
        new_df = relevant_tx.process_transaction(db_table)
        expected_sender = TestProcessor.ALGO_MAINNET_CONTRACT
        expected_receiver = TestProcessor.TEST_ALGO_ACCOUNT
        expected_transaction_id = "UBQVZLLCJVUEUMSWH6OS4D5NWQEE3ZFFGQUXZTBB4OFCQX6VPBEQ"
        expected_amount = 3000010
        expected_asset_id = 0
        expected_confirmed_round = 18933620
        expected_values = [expected_sender, expected_receiver, expected_confirmed_round, expected_amount, expected_asset_id, expected_transaction_id]
        actual_values = list(new_df.iloc[0])
        self.assertEqual(actual_values, expected_values)

    def test_borrow_transaction(self):
        """
        Tests seeing how borrow transactions are done
        Borrowed 2 usdc here https://algoexplorer.io/tx/group/YE2eY9KkdmASVJdxRKbFwzeeFd4u3Kxcvqy7HUkhQeM%3D
        """
        borrow_block_number = 18955092
        borrow_block = User().get_algorand_block(borrow_block_number)
        borrow_account_id = TestProcessor.TEST_ALGO_ACCOUNT
        borrow_by_account = borrow_block.get_transactions_by_account(borrow_account_id)
        borrow_relevant_tx = borrow_by_account[14]
        print("test!")
        withdraw_block_number = 18933620
        withdraw_block = User().get_algorand_block(withdraw_block_number)
        withdraw_account_id = TestProcessor.TEST_ALGO_ACCOUNT
        withdraw_by_account = withdraw_block.get_transactions_by_account(withdraw_account_id)
        withdraw_relevant_tx = withdraw_by_account[14]
        print("test!")
        withdraw_block_2 = 18955321
        withdraw_borrow_block_2 = User().get_algorand_block(withdraw_block_2)
        withdraw_borrow_account_id_2 = TestProcessor.TEST_ALGO_ACCOUNT
        withdraw_borrow_by_account_2 = withdraw_borrow_block_2.get_transactions_by_account(withdraw_borrow_account_id_2)
        withdraw_borrow_relevant_tx_2 = withdraw_borrow_by_account_2[14]
        print("test!")

    def test_repay_loan(self):
        """
        This transaction is repaying a loan
        https://algoexplorer.io/block/18955624
        """
        repay_block_number = 18955624
        block = User().get_algorand_block(repay_block_number)
        by_account = block.get_transactions_by_account(self.TEST_ALGO_ACCOUNT)
        print("TEST")

    def test_process_transactions(self):
        ALGO_CONTRACT_ID = "TY5N6G67JWHSMWFFFZ252FXWKLRO5UZLBEJ4LGV7TPR5PVSKPLDWH3YRXU"
        transactions_table_cols = ['sender', 'receiver', 'confirmed_round', 'amount', 'asset_id', 'transaction_id']
        db_table = pd.DataFrame(columns=transactions_table_cols)
        new_table = process_account_transactions(account_id=ALGO_CONTRACT_ID, db_table=db_table)
        print("Test!")

