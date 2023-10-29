"""
Bobble Sort 버블 정렬
- 바로 옆에 있는 값과 비교해서 작은것을 앞으로 보낸다
- 결과적으로 한번 반복을 했을때 가장 큰 값이 맨 뒤로 간다
- 효율이 가장 떨어짐
"""

sample = [2, 1, 6, 7, 5, 3, 4, 9, 8]


def bobble_sort(input: list[int]):
    temp = input.copy()
    for _ in range(0, len(input)):
        for index, value in enumerate(range(0, len(temp) - 1)):
            first, second = temp[index:index + 2]
            if first > second:
                temp[index], temp[index + 1] = temp[index + 1], temp[index]
    return temp


print(bobble_sort(sample))
