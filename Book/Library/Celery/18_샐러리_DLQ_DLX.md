## 샐러리 - DLQ, DLX

### DLQ (Dead Letter Queue)

    - A dead letter queue is a special queue where messages are sent when they cannot be delivered or processed
      successfully by consumers
    - 원인
        - regject by a consumer
        - not be acknowledged within a specified time frame (acknowledgment timeout)
        - error during process
    - 문제가 되는 메시지는 따라 모아서 처리할수 있기 때문에 중요하다

### DLX (Dead Letter Exchange)

- Publisher -> Event Queue -> Consumer -> DLQ
```python
@app.task(bind=True, queue='celery')
def is_positive_number(self, num:int):
    try:
        if num < 0:
            raise ValueError('num is negativef')
    except Exception as e:
        traceback_str = traceback.format_exc()
        handle_error.apply_asnyc(args=[self.request.id, str(e), traceback_str])

@app.task(queue="dlq")
def handle_error(task_id, exception, traceback_str):
    print(task_id)
    print(exception)
    print(traceback_str)
```