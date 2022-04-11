## Typed AlgorandIndexer API Wrapper
This Python package is a wrapper around the [AlgoExplorer Indexer API](https://algoexplorer.io/api-dev/indexer-v2), I'm not 
affiliated with them in anyway. What's useful about this package is that it wraps the API responses with fully typed nested 
data structures, so it's much easier to manipulate and explore the complex data structures related to the Algorand 
indexer than it would normally be. 

### Use cases
I had originally written some of this code when I was working on a liquidation bot for AlgoFi. In AlgoFI's case there is 
a decent enough python sdk anyway, but it is useful for any sort of analysis like that whether it be arbitraging, 
creating backtests for softare, doing on chain analyis to distribute airdrops, etc. 

### Installation
1. Clone the repo
2. Create a virtual environment `python3 -m venv .venv`
3. Install requirements `pip3 install -r requirements.txt`

### Using the API Client
The main API interface is in [algo_indexer_api_v2.py](algo_indexer_api_v2.py) and the data models are in [models](models).

Suppose you wanted to write some code to programattically check the state of an Algorand transaction here is an example:

```python
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
```

Where the output is:  
```commandline
Base Interest Rate: 25000000 
Active Collateral: 40461873672111
```

Rather than keep one eye on the documentation while you code it is easy to use the Python models as "code-as-documentation"
and use IDE text completion to do a lot of the work for you.   

### Paginating responses 
Paginating the responses is fairly trivial for the routes that support it. Here is an example: 

```python
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
```
This shows how to get all the balances for the akita inu token for example. You might want to collect this data to
analyze rates of people opting into the asset for example to get an idea of usage trends.

### Note on implementation of the models 
I used another project I had worked on that [generates nested Python classes from arbitrary](https://github.com/ianm199/dataClassUtil)
json data in order to create the code in [models](models). That project is still pretty early, so there is hack in 
the SubClass class in [utils.py](models/utils.py) that makes these nested classes actually get instantiated from the intial json.
It's not optimized at all, so this package is probably used better for prototyping than anything that is performance
intensive.

### TODO
I would consider this very much a first iteration. I would make some more updates if this gets some usage:
* Adding the "search" functionality from the 
* Dockerfile
* Setup.py
* PyPl support
* Proper CI/CD with the tests + github actions