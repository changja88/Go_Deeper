## 샐러리 - Task class
```python
class MyTask(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print()

@app.task(base=MyTask) # 등록을 하고 사용해야한다 
        
@app.task(base=MyTask)
def my_task():
    pass
```
- on_failure 를 비롯하여 많은 메소드를 오버라이드 하여 사용할 수 있다 