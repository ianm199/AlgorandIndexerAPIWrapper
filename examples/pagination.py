import pprint
from algo_indexer_api_v2 import APIUser


def get_balances_of_asset(asset_id: int) -> None:
    user = APIUser()
    balances = user.get_asset_balances(asset_id=asset_id)
    while (balances.next_token):
        pprint.pprint(balances.balances, indent=4)
        balances = user.get_asset_balances(asset_id=asset_id, next=balances.next_token)


if __name__ == '__main__':
    akita_inu_id = 384303832
    get_balances_of_asset(akita_inu_id)
