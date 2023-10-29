from collections import deque

"""
파이썬에서 큐 구현은 list를 사용하는 것보다 deque를 사용하는 것이 시간 복잡도 측면에서 더 좋다 
"""
queue = deque()

queue.append(5)
queue.append(4)
queue.append(3)
queue.append(2)
queue.append(1)
print(queue)
queue.popleft()
print(queue)
queue.popleft()
queue.popleft()
queue.popleft()
