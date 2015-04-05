#!/usr/bin/env python3

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

    for verb, iterator in grammar.items():
        for it in iterator:
            print(verb, *it)

    print('*')

def main():
    pairs = [
            ('emmanuel', 'emmaneul',),
            ('google', 'googre',),
            ('apple', 'arpre',),
            ('github', 'bituhbslong',),
    ]

    for pair in pairs:
        edit_distance(*pair)

if __name__ == '__main__':
    main()
