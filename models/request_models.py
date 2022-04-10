from dataclasses import dataclass, field
from models.algorand_transaction import AlgorandTransaction
from models.utils import SubClass
from typing import List

@dataclass
class AlgorandTransactionsReq(SubClass):
    SUBCLASSES = {'transactions': AlgorandTransaction}

    current_round: int
    transactions: List[AlgorandTransaction]
    next_token: str = field(default_factory=str)