from typing import List, Dict
from dataclasses import dataclass, field
from models.utils import convert_keys_to_snake_case
from models.algorand_transaction import AlgorandTransaction

@dataclass
class UpgradeVote:
    upgrade_approve: bool = field(default_factory=bool)
    upgrade_delay: int = field(default_factory=int)
    upgrade_propose: str = field(default_factory=str)

@dataclass
class UpgradeState:
    current_protocol: str = field(default_factory=str)
    next_protocol: str = field(default_factory=str)
    next_protocol_approvals: int = field(default_factory=int)
    next_protocol_switch_on: int = field(default_factory=int)
    next_protocol_vote_before: int = field(default_factory=int)

@dataclass
class Multisig:
    subsignature: List[Dict] = field(default_factory=list)
    threshold: int = field(default_factory=int)
    version: int = field(default_factory=int)

@dataclass
class MultisigSignature:
    subsignature: List[Dict] = field(default_factory=list)
    threshold: int = field(default_factory=int)
    version: int = field(default_factory=int)

@dataclass
class Logicsig:
    multisig_signature: MultisigSignature
    args: List[str] = field(default_factory=list)
    logic: str = field(default_factory=str)
    signature: str = field(default_factory=str)

@dataclass
class Signature:
    logicsig: Logicsig
    multisig: Multisig
    sig: str = field(default_factory=str)

@dataclass
class PaymentTransaction:
    amount: int = field(default_factory=int)
    close_amount: int = field(default_factory=int)
    close_remainder_to: str = field(default_factory=str)
    receiver: str = field(default_factory=str)

@dataclass
class KeyregTransaction:
    non_participation: bool = field(default_factory=bool)
    selection_participation_key: str = field(default_factory=str)
    vote_first_valid: int = field(default_factory=int)
    vote_key_dilution: int = field(default_factory=int)
    vote_last_valid: int = field(default_factory=int)
    vote_participation_key: str = field(default_factory=str)

@dataclass
class AssetTransferTransaction:
    amount: int = field(default_factory=int)
    asset_id: int = field(default_factory=int)
    close_amount: int = field(default_factory=int)
    close_to: str = field(default_factory=str)
    receiver: str = field(default_factory=str)
    sender: str = field(default_factory=str)

@dataclass
class AssetFreezeTransaction:
    address: str = field(default_factory=str)
    asset_id: int = field(default_factory=int)
    new_freeze_status: bool = field(default_factory=bool)

@dataclass
class Params:
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
class AssetConfigTransaction:
    params: Params
    asset_id: int = field(default_factory=int)

@dataclass
class GlobalStateSchema:
    num_uint: int = field(default_factory=int)
    num_byte_slice: int = field(default_factory=int)

@dataclass
class LocalStateSchema:
    num_uint: int = field(default_factory=int)
    num_byte_slice: int = field(default_factory=int)

@dataclass
class ApplicationTransaction:
    local_state_schema: LocalStateSchema
    global_state_schema: GlobalStateSchema
    on_completion: str = field(default_factory=str)
    application_args: List[str] = field(default_factory=list)
    accounts: List[str] = field(default_factory=list)
    foreign_apps: List[int] = field(default_factory=list)
    foreign_assets: List[int] = field(default_factory=list)
    approval_program: str = field(default_factory=str)
    clear_state_program: str = field(default_factory=str)
    extra_program_pages: int = field(default_factory=int)

@dataclass
class Transactions:
    application_transaction: ApplicationTransaction
    asset_config_transaction: AssetConfigTransaction
    asset_freeze_transaction: AssetFreezeTransaction
    asset_transfer_transaction: AssetTransferTransaction
    keyreg_transaction: KeyregTransaction
    signature: Signature
    payment_transaction: PaymentTransaction
    auth_addr: str = field(default_factory=str)
    close_rewards: int = field(default_factory=int)
    closing_amount: int = field(default_factory=int)
    confirmed_round: int = field(default_factory=int)
    created_application_index: int = field(default_factory=int)
    created_asset_index: int = field(default_factory=int)
    fee: int = field(default_factory=int)
    first_valid: int = field(default_factory=int)
    genesis_hash: str = field(default_factory=str)
    genesis_id: str = field(default_factory=str)
    group: str = field(default_factory=str)
    id: str = field(default_factory=str)
    intra_round_offset: int = field(default_factory=int)
    last_valid: int = field(default_factory=int)
    lease: str = field(default_factory=str)
    note: str = field(default_factory=str)
    receiver_rewards: int = field(default_factory=int)
    rekey_to: str = field(default_factory=str)
    round_time: int = field(default_factory=int)
    sender: str = field(default_factory=str)
    sender_rewards: int = field(default_factory=int)
    tx_type: str = field(default_factory=str)
    local_state_delta: List[Dict] = field(default_factory=list)
    global_state_delta: List[Dict] = field(default_factory=list)
    logs: List[str] = field(default_factory=list)
    inner_txns: List[str] = field(default_factory=list)


@dataclass
class Rewards:
    fee_sink: str = field(default_factory=str)
    rewards_calculation_round: int = field(default_factory=int)
    rewards_level: int = field(default_factory=int)
    rewards_pool: str = field(default_factory=str)
    rewards_rate: int = field(default_factory=int)
    rewards_residue: int = field(default_factory=int)

@dataclass
class AlgorandBlock:
    upgrade_state: UpgradeState
    upgrade_vote: UpgradeVote
    rewards: Rewards
    transactions: List[Transactions]
    genesis_hash: str = field(default_factory=str)
    genesis_id: str = field(default_factory=str)
    previous_block_hash: str = field(default_factory=str)
    round: int = field(default_factory=int)
    seed: str = field(default_factory=str)
    timestamp: int = field(default_factory=int)
    transactions_root: str = field(default_factory=str)
    txn_counter: int = field(default_factory=int)

    @classmethod
    def init_from_json(cls, json_dict: dict):
        new_dict = convert_keys_to_snake_case(json_dict)
        new_dict['transactions'] = list(
            map(lambda trans: AlgorandTransaction.init_from_json_dict(trans), new_dict['transactions']))
        new_dict['rewards'] = convert_keys_to_snake_case(new_dict['rewards'])
        return AlgorandBlock(**new_dict)