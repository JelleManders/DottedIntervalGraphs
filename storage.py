##
#  storage.py
#  Wrapper for the python pickle library to facilitate usage, the get_data()
#  function returns a list where the first element indicates failure or success.
#  In the latter case, the requested data is found on index 1.
#
#  @author Jelle Manders - github.com/jellemanders
#  @date   2017-11
##

import pickle

def get_data(path):
	try:
		with open(path, 'rb') as f:
			data = pickle.load(f)
			# print('found data -> '+path)
			return [True, data]
	except Exception:
		return [False]

def store_data(data, path):
	with open(path, 'wb') as f:
		pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
