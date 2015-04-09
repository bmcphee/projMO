#!/usr/bin/env python3

import sys

# Local modules
import constants
import cli_parser

import utils

NOOP  = 'n'
CHECK = 'c'
EXIT  = 'e'

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

def main():
    args, _ = cli_parser.cli_parser()

    default_fuzziness = args.fuzziness
    default_dict      = args.dict

    index = utils.read_and_index(default_dict)

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
                    cur_dict = read_and_index(rest[1])

            matches = utils.find_matches(query, fuzziness, cur_dict)

            if not matches:
                print('No matches!')
            else:
                print(matches)

if __name__ == '__main__':
    main()
