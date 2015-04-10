#!/usr/bin/env python3

DEBUG = False
penalties = dict(
    add=-2,
    delete=-2,
    keep=3,
    move=2
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

    for verb, iterator in grammar.items():
        penalty = penalties.get(verb, -1)
        rank += (penalty * len(iterator))

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
