from dataclasses import field, dataclass
from models.utils import SubClass


@dataclass
class Params(SubClass):
    clawback: str = field(default_factory=str)
    creator: str = field(default_factory=str)
    decimals: int = field(default_factory=int)
    default_frozen: bool = field(default_factory=bool)
    freeze: str = field(default_factory=str)
    manager: str = field(default_factory=str)
    metadata_hash: str = field(default_factory=str)
    name: str = field(default_factory=str)
    name_b64: str = field(default_factory=str)
    reserve: str = field(default_factory=str)
    total: int = field(default_factory=int)
    unit_name: str = field(default_factory=str)
    unit_name_b64: str = field(default_factory=str)
    url: str = field(default_factory=str)
    url_b64: str = field(default_factory=str)


@dataclass
class Asset(SubClass):
    SUBCLASSES = {"params": Params}

    params: Params
    index: int = field(default_factory=int)
    deleted: bool = field(default_factory=bool)
    created_at_round: int = field(default_factory=int)
    destroyed_at_round: int = field(default_factory=int)


@dataclass
class AlgorandAsset(SubClass):
    SUBCLASSES = {"asset": Asset}

    asset: Asset
    current_round: int
