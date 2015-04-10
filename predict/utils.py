#!/usr/bin/env python3

import doctest

# Local module
try:
	from .edit_distance import  edit_distance
	from .index    import Index
except:
	from edit_distance import  edit_distance
	from index    import Index

max_rank_cache = {}

def read_and_index(path):
	with open(path) as f:
		lines = f.readlines()
		r_lines = [l.rstrip().lstrip() for l in lines]
		index = Index(r_lines)

		return index

def percenter(rank, max_rank):
	"""
	>>> percenter(1, 0)
	100.0
	>>> percenter(0, 0)
	0.0
	>>> percenter(9, 10)
	90.0
	"""
	return 100 * (rank/(max_rank or 1))

def find_matches(query, fuzziness, index):
	if not query:
		return [(0, query)]

	max_rank = max_rank_cache.get(query, None)
	if max_rank is None: # Cache miss
		max_rank = edit_distance(query, query)
		max_rank_cache[query] = max_rank
	_, found = index[query]

	if found:
		return [(100, query,)]

	head = query[0]
	matches = []
	for item in index:
		if not item:
			continue

		if head == item[0]:
			rank = edit_distance(query, item)
			percent = percenter(rank, max_rank)
			if percent >= fuzziness:
				matches.append((percent, item))
			
	matches.sort(key=lambda a: a[0], reverse=True)
	return matches

def main():
	doctest.testmod()

if __name__ == '__main__':
	main()
