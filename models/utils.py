def convert_keys_to_snake_case(dict_to_fix: dict) -> dict:
    result = {}
    for key, value in dict_to_fix.items():
        new_key = key.replace("-", "_")
        result[new_key] = value
    return result