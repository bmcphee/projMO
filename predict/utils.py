#!/usr/bin/env python3

# Local module
try:
    from .edit_distance import  edit_distance
except:
    from edit_distance import  edit_distance

max_rank_cache = {}

def read_dict(path):
    index = []

    with open(path) as f:
        for line in f:
            line = line.rstrip().lstrip()

            if not line:
                continue

            index.append(line)
            
            # TODO: Index by first character or make a try
            # ch = line[0].lower()
            # index.setdefault(ch, []).append(line)

    return index

def percenter(rank, max_rank):
    return rank/(max_rank or 1)

def find_matches(query, fuzziness, index):
    max_rank = max_rank_cache.get(query, None)
    if max_rank is None: # Cache miss
        max_rank = edit_distance(query, query)
        max_rank_cache[query] = max_rank

    matches = []
    for item in index:
        rank = edit_distance(query, item)
        percent = percenter(rank, max_rank)
        if percent >= fuzziness:
            matches.append((percent, item))

    matches.sort(key=lambda a: a[0], reverse=True)
    return matches
