"""
insertion Sort (삽입 정렬)
- 각 숫자를 필요할 때만 특정 위치에 삽입 한다
- 각 숫자를 볼 때 앞에 것들은 정렬이 되어 있다고 가정한다
"""

sample = [2, 1, 6, 7, 5, 3, 4, 9, 8]


def merge_sort(input: list[int]):
    result = []
    for index in range(0, len(input)):
        if len(result) == 0:
            result.append(input[index])
        else:
            result = insert_item(result, input[index])
    return result


def insert_item(input_list: list[int], input_item: int):
    temp = []
    if input_list[0] > input_item:
        temp.append(input_item)
        temp.extend(input_list)
        return temp
    if input_list[-1] < input_item:
        temp.extend(input_list)
        temp.append(input_item)
        return temp

    for index, item in enumerate(input_list):
        temp.append(item)
        if index == len(input_list) - 1:
            return temp

        next_item = input_list[index + 1]
        if item < input_item < next_item:
            temp.append(input_item)

    return temp


a = merge_sort(sample)
print(a)
