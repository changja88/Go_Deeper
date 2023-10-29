"""
합병 정렬
- 분할 정복
- 정확히 반씩 나누기 떄문에 최악의 경우가 없다
"""

sample = [2, 1, 6, 7, 5, 3, 4, 9, 8]


def merge(left: list[int], right: list[int]) -> list[int]:
    result = []
    left_index, right_index = 0, 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] < right[right_index]:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    if left_index == len(left):
        result.extend(right[right_index:])
    else:
        result.extend(left[left_index:])

    return result


def merge_sort(input: list[int]):
    if len(input) == 1:
        return input

    div = len(input) // 2
    left = merge_sort(input[:div])
    right = merge_sort(input[div:])

    result = merge(left, right)
    return result


a = merge_sort(sample)
print(a)
