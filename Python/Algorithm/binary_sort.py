sample = [0, 1, 2, 3, 4, 6, 7, 8, 9, 10]  # 10개


def binary_search(input: list[int], target, start_index, end_index):
    mid_index = (start_index + end_index) // 2
    if input[mid_index] == target:
        return mid_index

    if input[mid_index] > target:
        return binary_search(input, target, start_index, mid_index - 1)
    else:
        return binary_search(input, target, mid_index + 1, end_index)


a = binary_search(sample, 2, 0, len(sample) - 1)
print(a)
