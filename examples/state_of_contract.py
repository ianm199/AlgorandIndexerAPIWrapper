from algo_indexer_api_v2 import APIUser
import base64

def get_variable_state_for_application(application_id: int, variable_key: str) -> str:
    """
    Example to show getting the varible state of an application
    """
    user = APIUser()
    application = user.get_algorand_application(application_id=application_id)
    for items in application.application.params.global_state:
        actual_key = decode_b64_string(items.key)
        if actual_key == variable_key:
            if items.value.uint:
                return items.value.uint
            else:
                return decode_b64_string(items.value.bytes)

def decode_b64_string(b64_s: str) -> str:
    return base64.b64decode(b64_s).decode("UTF-8")

if __name__ == '__main__':
    algofi_mainet_algo_application = 465814065
    nb_var = get_variable_state_for_application(algofi_mainet_algo_application, 'nb') # Corresponds to base interest rate
    ab_var = get_variable_state_for_application(algofi_mainet_algo_application, 'acc') # Corresponds to active collateral
    print(f"Base Interest Rate: {nb_var} \nActive Collateral: {ab_var}")