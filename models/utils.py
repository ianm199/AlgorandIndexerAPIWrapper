import pprint


def convert_keys_to_snake_case(dict_to_fix: dict) -> dict:
    result = {}
    for key, value in dict_to_fix.items():
        new_key = key.replace("-", "_")
        result[new_key] = value
    return result





class SubClass:
	"""
	Not meant to be instantiated directly, this class enables other classes to be recursively instantiated so that
	you can make a deeply nested fully typed call such as
	AlgorandTransaction.application_transaction.local_state_schema.num_byte_slice and have it work

	I think this could be improved by digging into the python dataclasses API a bit, just an initial hack
	"""

	SUBCLASSES = {}

	@classmethod
	def init_from_json_dict(cls, json_dict: dict):
		"""
		This is a bit of Python magic neccesary to actually instantiate deeply nested python data structures. From a
		performance perspective there is a lot to be done here to improve, this is intended to mainly enable as readable
		and useable code as possible for now
		:param json_dict: arbitrary json dict data. The data schema should match the schema of the subclass or it
		will throw a KeyError
		:return:
		"""
		new_dict = convert_keys_to_snake_case(json_dict)
		for key in new_dict:
			if key in cls.SUBCLASSES:
				if type(new_dict[key]) == dict:
					new_dict[key] = convert_keys_to_snake_case(new_dict[key])
					new_dict[key] = cls.SUBCLASSES[key].init_from_json_dict(new_dict[key])
				elif type(new_dict[key]) == list:
					pprint.pprint(new_dict[key])
					new_dict[key] = list(map(lambda listDicts: cls.SUBCLASSES[key].init_from_json_dict(listDicts), new_dict[key]))
		pprint.pprint(new_dict, indent=4)
		return cls(**new_dict)


