"""
Quick Sort
- 대표적인 분할 정복 알고리즘
- 기준 값(보통 맨 앞)을 정하고
"""
sample = [2, 1, 6, 7, 5, 3, 4, 9, 8]


def quick_sort(input: list[int], start, end):
    if start >= end:
        return

    pivot = start
    left = start + 1
    right = end
    while (left <= right):
        while (left <= end and input[left] <= input[pivot]):
            left += 1
        while (right > start and input[right] > input[pivot]):
            right -= 1
        if (left > right):
            input[right], input[pivot] = input[pivot], input[right]
        else:
            input[right], input[left] = input[left], input[right]

    quick_sort(input, start, right - 1)
    quick_sort(input, right + 1, end)


quick_sort(sample, 0, len(sample) - 1)
print(sample)
