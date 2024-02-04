from typing import List


def solve(nums: List[int], target: int) -> List[int]:
    """
    По памяти:
        1. словарь с позициями чисел из nums - тоже n, т.к. количество ключей не больше n,
        а общее количество элементов в списках равно n.
        Итого по памяти: O(n)
    По времени:
        1. nums_pos формируем за n.
        2. поиск позиции (несмотря на то, что там двойной цикл) тоже за n,
        т.к. в первом цикле мы в худшем случае потратим n времени,
        а во втором сделаем не более 2-х шагов. Т.е. время итоговое n.
        Итого по времени: O(n)
    """
    nums_pos: dict[int, list[int]] = dict()
    for i, num in enumerate(nums):
        nums_pos.setdefault(num, []).append(i)
    for i, num in enumerate(nums):
        for k in nums_pos.get(target - num, []):
            if k != i:
                return [i, k]

    return [-1, -1]
