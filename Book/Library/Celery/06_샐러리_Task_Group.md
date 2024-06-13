## 샐러리 - Task Group
- 그루핑 방법
  - Group : 테스크 병렬 실행
  - Chain : 테스크 연결, 하나하나 실행
  - Chord : Group with a callback
  - Starmap : a single task with a list of argument tuple 
- Signature
  - a way to encapsulate information about a task to be executed
  - 작업의 실행방법, 인수, 옵션 등을 정의하며, 이를 통해 체인으로 연결하거나 그룹화할 수 있다

#### group 사용법
```python
from celery import group, signature

job = group(signature('worker.tasks.add', args=(i, i) for i in range(10)))
result = job.apply_async()

job = group(add.s(i, i) for i in range(10)) # 숏컷
result = job.apply_async()
```
#### chain 사용법
```python
from celery import chain

workflow = chain(add.s(2, 2), add.s(4), add.s(8))
result = workflow.apply_aync()
result.get() # 16
```
#### chord 사용법
```python
@shared_task(queue='celery')
def xsum(numbers):
    return sum(numbers)


callback = xsum.s()
header = [add.s(i, i) for i in range(10)]
result = chord(header)(callback)
result.get()  # 90
```
#### starmap 사용법
```python
result = add.startmap(zip(range(10), range(10))).apply_async()
result.get() # [0,2,4,6,8,10,12,14,16,18]
```