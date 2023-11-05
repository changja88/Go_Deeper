"""
힙 정렬
- Heap Tree structure 구조를 이용한다
- 이진트리가 사용된다
- 완전 이진트리 : 데이터가 왼쪽부터 오른쪽으로 차있는 상태 (맨아래 맨 오른쪽은 비어있을수 있다)
- 최솟값이나 최댓값ㅇ을 빠르게 찾아내기 위해서 완전 이진트리를 사용한다

- 힙 생성알고리즘
    - 자식이 부모보다 큰 노드의 경우 부모와 자식을 바꿔준다
"""
sample = [
    2,
    1, 6,
    7, 5, 3, 4,
    # 9, 8
]


def heap_sort1(unsorted):
    n = len(unsorted)
    # 최대 힙 만들기
    # 최소힙은 부등호만 반대로 바꿔주면 됨
    for i in range(1, n):
        chiled_index = i
        while chiled_index != 0:
            parent_index = (chiled_index - 1) // 2
            if unsorted[parent_index] < unsorted[chiled_index]:
                unsorted[parent_index], unsorted[chiled_index] = unsorted[chiled_index], unsorted[parent_index]
            chiled_index = parent_index  # 최대값이 루트까지 도달 할 수 있도록

    # 힙 만들기
    for node in range(n - 1, -1, -1):
        # 루트 노드와 마지막 노드를 교환
        # 값이 큰 순서대로 힙의 끝에 저장됨
        unsorted[0], unsorted[node] = unsorted[node], unsorted[0]
        parent_index = 0
        chiled_index = 1

        # 정렬이 미완료 된 노드들 사이에서
        # 마지막 노드 자리리 보내준 루트 노드를 제외한 가장 큰 값을 찾고
        # 루트 노드 자리로 온 마지막 노드의 자리 찾기
        while chiled_index < node:
            chiled_index = parent_index * 2 + 1
            # 마지막 노드 자리로 보낸 루트 노드를 제외한 가장 큰 노드를 찾기 위해
            if chiled_index < node - 1 and unsorted[chiled_index] < unsorted[chiled_index + 1]:
                chiled_index += 1
            # 마지막 노드 자리로 보낸 루트 노드를 제외한 가장 큰 노드를 루트 자리로 보내기 위한 과정
            if chiled_index < node and unsorted[parent_index] < unsorted[chiled_index]:
                unsorted[parent_index], unsorted[chiled_index] = unsorted[chiled_index], unsorted[parent_index]

            parent_index = chiled_index

    return unsorted


heap_sort1(sample)
print(sample)
