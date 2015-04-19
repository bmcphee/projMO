#!/usr/bin/env python3

DEBUG = False
Infinity = float('inf')

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

EqualTo     = 0
LessThan    = -1
GreaterThan = 1

def compare(a, b):
    if a == b:
        return EqualTo
    if a < b:
        return LessThan
    return GreaterThan

def __sorted_search(query, content):
    mid = 0
    low, high = 0, len(content) - 1

    found = False

    while low <= high:
        mid = (low + high) >> 1

        comparison = compare(content[mid], query)
        if comparison == EqualTo:
            found = True
            break

        if comparison == LessThan:
            low = mid + 1
        else:
            high = mid - 1

    return low, mid, high, found

def valley_search(query, content):
    return __sorted_search(query, content)

def binary_search(query, content):
    _, mid, _, found = __sorted_search(query, content)
    if not found:
        return -1
    return mid

def edit_distance(base, subject, ranger=__sorted_search):
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

    subject_index = {}
    for j, ch2 in enumerate(subject):
        subject_index.setdefault(ch2, {})[j] = j

    for subj_ch, subj_index_map in subject_index.items():
        base_indices_list = index.get(subj_ch, None)

        if base_indices_list is None:
            # No single character like this exists in the base -- deletions
            for i in subj_index_map:
                deletions.append((i, subj_ch,))
            continue

        # Find exact matches first
        exact_matches = []
        for i in subj_index_map:
            item_index = binary_search(i, base_indices_list)
            if item_index >= 0:
                exact_matches.append(i)
                base_indices_list.pop(item_index)

        for i in exact_matches:
            inplace.append((i, i, subj_ch))
            subj_index_map.pop(i)

        # Next step is to find an index with minimal distance for a move
        best_match = Infinity
        best_index = 0
        base_index = -1
        raw_base_index = -1

        for i in subj_index_map:
            low, _, high, _ = valley_search(i, base_indices_list)
            
            low_diff = high_diff = Infinity
            base_len = len(base_indices_list)
            low_index = high_index = Infinity

            if high >= 0 and high < base_len:
                high_index = base_indices_list[high]
                high_diff = abs(i - high_index)
            if low < base_len:
                low_index = base_indices_list[low]
                low_diff = abs(i - low_index)

            best = low_diff
            l_m = low_index
            raw_base_index = low
            if low_diff > high_diff:
                best = high_diff
                l_m = high_index
                raw_base_index = high

            # print('low_diff', low_diff, low, 'high_diff', high_diff, high, i)
            if best < best_match: 
                # print('changing', best, best_match, subj_ch)
                best_match = best
                best_index = i
                base_index = l_m

        # print('\033[47moverall_best_match', best_match, '\033[00m', best_index, base_index)
        # Match up the closest index to a mismatched character
        if best_match < Infinity and best_index < Infinity:
            base_indices_list.pop(raw_base_index)
            moves.append((best_index, base_index, subj_ch,)) 
            subj_index_map.pop(best_index)

        # From then on, open season, greedily match up the first available slot
        # for moving or mark as a deletion in case base_indices_list is empty
        while subj_index_map:
            i, _ = subj_index_map.popitem()
            if not base_indices_list:
                deletions.append((i, subj_ch,))
                continue

            low, _, high, _ = valley_search(i, base_indices_list)
            sub = high
            if sub < 0:
                sub = low

            item_index = base_indices_list.pop(sub)
            moves.append((i, item_index, subj_ch,)) 

    for ch, base_indices_list in index.items():
        for base_index in base_indices_list:
            additions.append((base_index, ch,))

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
            ('github', 'bituhxbslong',),
            ('fithub', 'gihtub',),
            ('fithub', 'fithub',),
            ('generic_code_is_here', 'generics_and_templating',),
            ('lebron_james', 'leroy_jenkins',),
            ('anagram', 'granmaa',),
    ]

    for pair in pairs:
        print(pair, edit_distance(*pair))

if __name__ == '__main__':
    main()
