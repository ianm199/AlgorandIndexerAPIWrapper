from dataclasses import field, dataclass
from typing import List, Dict
from enum import Enum
from models.utils import convert_keys_to_snake_case


ASSET_TRANSFER_TRANSACTION = 'asset-transfer-transaction'
APPLICATION_TRANSACTION = "application-transaction"
PAYMENT_TRANSACTION = "payment-transaction"
TRANSACTION = "transaction"

@dataclass
class LocalStateSchema:
	num_byte_slice: int = field(default_factory=int)
	num_uint: int = field(default_factory=int)

@dataclass
class GlobalStateSchema:
	num_byte_slice: int = field(default_factory=int)
	num_uint: int = field(default_factory=int)

@dataclass
class Signature:
	sig: str = field(default_factory=str)

@dataclass
class PaymentTransaction:
	amount: int = field(default_factory=int)
	close_amount: int = field(default_factory=int)
	receiver: str = field(default_factory=str)

@dataclass
class AssetTransferTransaction:
	amount: int = field(default_factory=int)
	asset_id: int = field(default_factory=int)
	close_amount: int = field(default_factory=int)
	receiver: str = field(default_factory=str)


@dataclass
class ApplicationTransaction:
	local_state_schema: LocalStateSchema
	global_state_schema: GlobalStateSchema
	accounts: List = field(default_factory=list)
	application_args: List[str] = field(default_factory=list)
	application_id: int = field(default_factory=int)
	foreign_apps: List[int] = field(default_factory=list)
	foreign_assets: List = field(default_factory=list)
	on_completion: str = field(default_factory=str)

@dataclass
class AlgorandTransaction:
	signature: Signature
	payment_transaction: PaymentTransaction = field(default_factory=dict)
	asset_transfer_transaction: AssetTransferTransaction = field(default_factory=dict)
	application_transaction: ApplicationTransaction = field(default_factory=dict)
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

	@classmethod
	def init_from_json_dict(cls, json_dict: dict):
		new_dict = convert_keys_to_snake_case(json_dict)

		if ASSET_TRANSFER_TRANSACTION in json_dict or ASSET_TRANSFER_TRANSACTION.replace("-", "_") in json_dict:
			new_dict['transaction'] = new_dict[ASSET_TRANSFER_TRANSACTION.replace("-", "_")]
			new_dict['transaction_type'] = ASSET_TRANSFER_TRANSACTION
			del new_dict[ASSET_TRANSFER_TRANSACTION.replace("-", "_")]

		elif APPLICATION_TRANSACTION in json_dict or APPLICATION_TRANSACTION.replace("-", "_") in json_dict:
			new_dict['transaction'] = new_dict[APPLICATION_TRANSACTION.replace("-", "_")]
			new_dict['transaction_type'] = APPLICATION_TRANSACTION
			del new_dict[APPLICATION_TRANSACTION.replace("-", "_")]

		elif PAYMENT_TRANSACTION in json_dict or PAYMENT_TRANSACTION.replace("-", "_") in json_dict:
			new_dict['transaction'] = new_dict[PAYMENT_TRANSACTION.replace("-", "_")]
			new_dict['transaction_type'] = PAYMENT_TRANSACTION
			del new_dict[PAYMENT_TRANSACTION.replace("-", "_")]

		else:
			raise ValueError(f"Unsupported tx type: {json_dict}")

		return AlgorandTransaction(**new_dict)

# @dataclass
# class AlgorandTransaction:
# 	transaction: Transaction
# 	current_round: int = field(default_factory=int)


