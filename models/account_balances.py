from dataclasses import dataclass, field
from typing import List
from models.utils import SubClass


@dataclass
class Balances(SubClass):
    address: str = field(default_factory=str)
    amount: int = field(default_factory=int)
    is_frozen: bool = field(default_factory=bool)
    deleted: bool = field(default_factory=bool)
    opted_in_at_round: int = field(default_factory=int)
    opted_out_at_round: int = field(default_factory=int)


@dataclass
class AccountBalanceReq(SubClass):

    SUBCLASSES = {"balances": Balances}

    balances: List[Balances]
    current_round: int = field(default_factory=int)
    next_token: str = field(default_factory=str)
