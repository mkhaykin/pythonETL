from is_broken import isBrokenVersion


def solve(n: int) -> int:
    """
        Решение через бинарный поиск, поэтому по времени: O(log(n)),
        дополнительная память используется только для границ, т.е. по памяти: O(1)
    """
    li: int = 1
    ri: int = n
    while li < ri:
        i = (li + ri) // 2
        if isBrokenVersion(i):
            ri = i
        else:
            li = i + 1

    return li
