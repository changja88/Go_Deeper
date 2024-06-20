## 샐러리 - task failure
```python
@task_failure.connect(sender=add)
def task_failure_handler(sender, task_id, exception, args, kwargs, traceback, einfo, **kwargs, **kwargs_extra):
    task_failure_clean_up.delay(task_id=task_id) # task_failure_clean_up 있는 함수 아님
```
- task_failure 데코레이터를 사용해서 테스크가 실패 했을때 연결해서 특정 테스크를 실행 시킬수 있다 