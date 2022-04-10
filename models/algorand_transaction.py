from dataclasses import field, dataclass
from typing import List, Dict
from models.utils import SubClass

ASSET_TRANSFER_TRANSACTION = 'asset-transfer-transaction'
APPLICATION_TRANSACTION = "application-transaction"
PAYMENT_TRANSACTION = "payment-transaction"
TRANSACTION = "transaction"


@dataclass
class Value(SubClass):
	action: int = field(default_factory=int)
	uint: int = field(default_factory=int)

@dataclass
class GlobalStateDelta(SubClass):

	SUBCLASSES = {'value': Value}

	value: Value
	key: str = field(default_factory=str)

@dataclass
class LocalStateDelta(SubClass):
	address: str = field(default_factory=str)
	delta: List[Dict] = field(default_factory=list)

@dataclass
class LocalStateSchema(SubClass):
	num_byte_slice: int = field(default_factory=int)
	num_uint: int = field(default_factory=int)

@dataclass
class GlobalStateSchema(SubClass):
	num_byte_slice: int = field(default_factory=int)
	num_uint: int = field(default_factory=int)

@dataclass
class Signature(SubClass):
	sig: str = field(default_factory=str)

@dataclass
class PaymentTransaction(SubClass):
	amount: int = field(default_factory=int)
	close_amount: int = field(default_factory=int)
	receiver: str = field(default_factory=str)

@dataclass
class AssetTransferTransaction(SubClass):
	amount: int = field(default_factory=int)
	asset_id: int = field(default_factory=int)
	close_amount: int = field(default_factory=int)
	receiver: str = field(default_factory=str)
	close_to: str = field(default_factory=str)


@dataclass
class ApplicationTransaction(SubClass):
	SUBCLASSES = {"local_state_schema": LocalStateSchema, "global_state_schema": GlobalStateSchema}

	local_state_schema: LocalStateSchema
	global_state_schema: GlobalStateSchema
	accounts: List = field(default_factory=list)
	application_args: List[str] = field(default_factory=list)
	application_id: int = field(default_factory=int)
	foreign_apps: List[int] = field(default_factory=list)
	foreign_assets: List = field(default_factory=list)
	on_completion: str = field(default_factory=str)

@dataclass
class AlgorandTransaction(SubClass):
	SUBCLASSES = {'payment_transaction': PaymentTransaction, 'asset_transfer_transaction': AssetTransferTransaction,
				 'application_transaction': ApplicationTransaction,
				 'local_state_delta': LocalStateDelta, 'global_state_delta': GlobalStateDelta}

	signature: Signature
	payment_transaction: PaymentTransaction = field(default_factory=dict)
	asset_transfer_transaction: AssetTransferTransaction = field(default_factory=dict)
	application_transaction: ApplicationTransaction = field(default_factory=dict)
	global_state_delta: GlobalStateDelta = field(default_factory=dict)
	local_state_delta: List[LocalStateDelta] = field(default_factory=list)
	close_rewards: int = field(default_factory=int)
	closing_amount: int = field(default_factory=int)
	confirmed_round: int = field(default_factory=int)
	fee: int = field(default_factory=int)
	first_valid: int = field(default_factory=int)
	genesis_hash: str = field(default_factory=str)
	genesis_id: str = field(default_factory=str)
	group: str = field(default_factory=str)
	id: str = field(default_factory=str)
	intra_round_offset: int = field(default_factory=int)
	last_valid: int = field(default_factory=int)
	receiver_rewards: int = field(default_factory=int)
	round_time: int = field(default_factory=int)
	sender: str = field(default_factory=str)
	sender_rewards: int = field(default_factory=int)
	tx_type: str = field(default_factory=str)
	transaction_type: str = field(default_factory=str)
	note: str = field(default_factory=str)
	lease: str = field(default_factory=str)




# @dataclass
# class AlgorandTransaction:
# 	transaction: Transaction
# 	current_round: int = field(default_factory=int)
