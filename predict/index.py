#!/usr/bin/env python3

import doctest

class Index:
	def __init__(self, item_list=[]):
		"""
		>>> items = ['rogue', 'bank', 'crank', 'dream', 'gem', '24']
		>>> index = Index(items)
		>>> index._index()
		>>> found = index['bank']
		>>> print(found)
		('bank', True)
		>>> found = index['Bank']
		>>> print(found)
		(None, False)
		"""
		# TODO: Should we make a copy of the data??
		self.__item_list = item_list
		self.__exact_matcher = {}
		self._index()

	def _index(self):
		for item_index, key in enumerate(self.__item_list):
			if not key:
				continue

			head = key[0]
			self.__exact_matcher.setdefault(head, {}).setdefault(len(key), []).append(item_index)

	def __iter__(self):
		return self.__item_list.__iter__()


	def __getitem__(self, key):
		not_found = (None, False,)
		if not key:
			return not_found
		head = key[0]
		cache_by_len = self.__exact_matcher.get(head, None)
		if not cache_by_len:
			return not_found

		key_len = len(key)
		match_index_list = cache_by_len.get(key_len, None)
		if not match_index_list:
			return not_found

		end_index = key_len - 1
		for index in match_index_list:
			possible_match = self.__item_list[index]

			if possible_match[end_index] != key[end_index]: # Last chars don't match!
				continue
			elif possible_match == key:
				return possible_match, True

		return not_found

def main():
	doctest.testmod()

if __name__ == '__main__':
	main()
