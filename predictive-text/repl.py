#!/usr/bin/env python3

import sys

# Local modules
import constants
import cli_parser
from edit_distance import  edit_distance

NOOP  = 'n'
CHECK = 'c'
EXIT  = 'e'

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

def tokenize(line, separator=' '):
    line = line.split(separator)
    return [field for field in line]

def read_line():
    return input('$ (exit with: %s) \033[47mquery [percentage dictfile]\033[00m '%(constants.EXIT_CHAR)).strip('\n')

def exit_like(ch):
    return ch and (ch[0] == constants.EXIT_CHAR)

def read_line_tokenize():
    tokens = tokenize(read_line())
    t_len = len(tokens)

    if t_len < 1:
        return NOOP, tokens

    if t_len == 1:
        head = tokens[0]
        if exit_like(head):
            return EXIT, head

    return CHECK, tokens

def exit():
    print('Bye!')
    sys.exit(-1)

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

    matches.sort(key=lambda a: a[0])
    return [item[1] for item in matches]

def main():
    args, _ = cli_parser.cli_parser()

    default_fuzziness = args.fuzziness
    default_dict      = args.dict

    index = read_dict(default_dict)

    reading = True
    while reading:
        action, tokens = read_line_tokenize()

        if action == EXIT:
            return exit()

        if action == CHECK:
            query     = tokens[0]
            fuzziness = default_fuzziness 
            cur_dict  = index

            length = len(tokens)
            if length >= 2:
                _, *rest = tokens
                fuzziness = float(rest[0])
                rest_len = len(rest)
                if rest_len >= 2:
                    cur_dict = read_dict(rest[1])

            matches = find_matches(query, fuzziness, cur_dict)

            if not matches:
                print('No matches!')
            else:
                print(matches)

if __name__ == '__main__':
    main()
