"""
Selection Sort (정렬 알고리즘)
- 가장 작은 것을 선택해서 앞으로 보낸다
"""

smaple = [2, 5, 6, 7, 1, 3, 4, 9, 8]


def selection_sort(input: list[int]):
    result = []
    temp = input.copy()
    for _ in range(0, len(input)):
        min = get_min(temp)
        result.append(min)
        temp.remove(min)


def get_min(input: list[int]):
    min = None

    for item in input:
        if min == None:
            min = item
        elif item < min:
            min = item
    return min


selection_sort(smaple)
