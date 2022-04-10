

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
	args: List[str] = field(default_factory=list)
	logic: str = field(default_factory=str)
	multisig_signature: MultisigSignature
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
	asset_id: int = field(default_factory=int)
	params: Params

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
	application_id: int = field(default_factory=int)
	on_completion: str = field(default_factory=str)
	application_args: List[str] = field(default_factory=list)
	accounts: List[str] = field(default_factory=list)
	foreign_apps: List[int] = field(default_factory=list)
	foreign_assets: List[int] = field(default_factory=list)
	local_state_schema: LocalStateSchema
	global_state_schema: GlobalStateSchema
	approval_program: str = field(default_factory=str)
	clear_state_program: str = field(default_factory=str)
	extra_program_pages: int = field(default_factory=int)

@dataclass
class Transactions:
	application_transaction: ApplicationTransaction
	asset_config_transaction: AssetConfigTransaction
	asset_freeze_transaction: AssetFreezeTransaction
	asset_transfer_transaction: AssetTransferTransaction
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
	keyreg_transaction: KeyregTransaction
	last_valid: int = field(default_factory=int)
	lease: str = field(default_factory=str)
	note: str = field(default_factory=str)
	payment_transaction: PaymentTransaction
	receiver_rewards: int = field(default_factory=int)
	rekey_to: str = field(default_factory=str)
	round_time: int = field(default_factory=int)
	sender: str = field(default_factory=str)
	sender_rewards: int = field(default_factory=int)
	signature: Signature
	tx_type: str = field(default_factory=str)
	local_state_delta: List[Dict] = field(default_factory=list)
	global_state_delta: List[Dict] = field(default_factory=list)
	logs: List[str] = field(default_factory=list)
	inner_txns: List[str] = field(default_factory=list)

@dataclass
class AccountBalanceReq:
	current_round: int = field(default_factory=int)
	next_token: str = field(default_factory=str)
	transactions: List[Transactions]




