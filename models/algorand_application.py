from dataclasses import field, dataclass
from typing import List, Dict
from models.utils import SubClass

@dataclass
class LocalStateSchema(SubClass):
    num_byte_slice: int = field(default_factory=int)
    num_uint: int = field(default_factory=int)


@dataclass
class GlobalStateSchema(SubClass):
    num_byte_slice: int = field(default_factory=int)
    num_uint: int = field(default_factory=int)


@dataclass
class Params(SubClass):
    SUBCLASSES = {"global_state_schema": GlobalStateSchema, "local_state_schmea": LocalStateSchema}

    global_state_schema: GlobalStateSchema
    local_state_schema: LocalStateSchema
    approval_program: str = field(default_factory=str)
    clear_state_program: str = field(default_factory=str)
    creator: str = field(default_factory=str)
    extra_program_pages: int = field(default_factory=int)
    global_state: List[Dict] = field(default_factory=list)


@dataclass
class Application(SubClass):
    SUBCLASSES = {"params": Params}

    params: Params
    created_at_round: int = field(default_factory=int)
    deleted: bool = field(default_factory=bool)
    id: int = field(default_factory=int)


@dataclass
class AlgorandApplication(SubClass):
    SUBCLASSES = {"application": Application}

    application: Application
    current_round: int = field(default_factory=int)
