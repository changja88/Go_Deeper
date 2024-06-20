## 샐러리 - time limit / timeout

- Task drivver -> Task
    - Task가 수행할수 있는 총 시간 : time limit
    - Task가 결과를 반환할수 있는 최대 시간 : timeout
        - 시간안에 결과를 반환하지 못해도 task자체는 성공적다로 끝났을 수도 있다

```python
@app.task(queue='celery', time_limit=5)
def long_runing_job():
    time.seep(10)
    print("aaaa")
```
- 위 테스크는 에러가 발생한다 -> 작업은 10초 걸리는데 리밋은 5초 이기 떄문에


```python
def simulating_timeout():
    result = long_running_job.delay()
    result.get(timeout=3) # 결과를 기다리는데 최대 3초 쓰겠다는 뜻
```
- 최종 결과 long_running_job 자체는 성공적으로 끝나지만 simulating_timeout자체는 실패한다 