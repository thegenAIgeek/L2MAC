def decimal_to_binary(decimal):
	"""You will be given a number in decimal form and your task is to convert it to
	binary format. The function should return a string, with each character representing a binary
	number. Each character in the string will be '0' or '1'.

	There will be an extra couple of characters 'db' at the beginning and at the end of the string.
	The extra characters are there to help with the format.

	Examples:
	decimal_to_binary(15)   # returns "db1111db"
	decimal_to_binary(32)   # returns "db100000db"
	"""
	if not isinstance(decimal, int):
		raise ValueError('Input must be an integer')
	binary = bin(decimal)[2:]
	return 'db' + binary + 'db'

def test_decimal_to_binary():
	assert decimal_to_binary(15) == 'db1111db'
	assert decimal_to_binary(32) == 'db100000db'
	assert decimal_to_binary(2) == 'db10db'
	assert decimal_to_binary(8) == 'db1000db'
	assert decimal_to_binary(0) == 'db0db'
