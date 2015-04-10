#!/usr/bin/env python3

DEBUG = False

def add_penalty(seq, *rest):
    return -1 * len(seq)

def delete_penalty(seq, *rest):
    return -1 * len(seq)

def move_penalty(seq, *args):
    max_penalty = 2
    scale_len = args[0] or 1
    total_rank = 0
    for k in seq:
        src_index, dest_index, *rest = k
        index_diff = abs(src_index - dest_index)
        penalty = (max_penalty - max_penalty * (index_diff/scale_len))
        # print('\033[92m', src_index, dest_index, '\033[00m', index_diff, scale_len, penalty)
        total_rank += penalty
    return total_rank

def keep_penalty(seq, *rest):
    return 3 * len(seq)

penalties = dict(
    add=add_penalty,
    delete=delete_penalty,
    keep=keep_penalty,
    move=move_penalty,
)

def edit_distance(base, subject):
    """
    Sequence of edits needed to transform the subject into the base
    """

    index = {}
    for i, ch1 in enumerate(base):
        index.setdefault(ch1, []).append(i)

    additions = []
    deletions = []
    inplace   = []
    moves     = []

    grammar = dict(
            move=moves,
            add=additions,
            keep=inplace,
            delete=deletions,
    )

    for j, ch2 in enumerate(subject):
        positions = index.get(ch2, None)
        if not positions:
            additions.append((j, ch2,))
            continue

        head = positions.pop(0)
        if head == j:
            inplace.append((j, ch2,))
        else:
            moves.append((head, j, ch2))

        if not positions:
            index.pop(ch2, None)

    for ch, positions in index.items():
        for position in positions:
            deletions.append((position, ch))

    rank = 0

    subject_len = len(subject)
    for verb, iterator in grammar.items():
        penalty_func = penalties.get(verb, None)
        rank += penalty_func(iterator, subject_len)

        if DEBUG: # 
            for it in iterator:
                print(verb, *it)

    if DEBUG:
        print('*\nrank ', rank)

    return rank

def main():
    global DEBUG
    DEBUG = True

    pairs = [
            ('brennan', 'bnrnane',),
            ('emmanuel', 'emmaneul',),
            ('emmanuel', 'emmanuel',),
            ('google', 'googre',),
            ('apple', 'arpre',),
            ('github', 'bituhbslong',),
    ]

    for pair in pairs:
        print(pair, edit_distance(*pair))

if __name__ == '__main__':
    main()
