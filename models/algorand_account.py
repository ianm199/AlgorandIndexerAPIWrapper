from dataclasses import dataclass, field
from models.utils import SubClass
from typing import List, Dict


@dataclass
class Account(SubClass):
    """
    This shows a flaw with the class generator, going to come back to this
    """
    address: str = field(default_factory=str)
    amount: int = field(default_factory=int)
    amount_without_pending_rewards: int = field(default_factory=int)
    assets: List[Dict] = field(default_factory=list)
    created_at_round: int = field(default_factory=int)
    deleted: bool = field(default_factory=bool)
    pending_rewards: int = field(default_factory=int)
    reward_base: int = field(default_factory=int)
    rewards: int = field(default_factory=int)
    round: int = field(default_factory=int)
    status: str = field(default_factory=str)
    total_apps_opted_in: int = field(default_factory=int)
    total_assets_opted_in: int = field(default_factory=int)
    total_created_apps: int = field(default_factory=int)
    total_created_assets: int = field(default_factory=int)


@dataclass
class AlgorandAccount(SubClass):

    SUBCLASSES = {"account": Account}

    account: Account
    current_round: int = field(default_factory=int)
