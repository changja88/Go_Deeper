## 샐러리 - Linking
```python
add.apply_async((2, 2), link=add.s(16))
```
- 하나의 테스크가 다른 테스크를 따라 가는 것

```python
@app.task(queue='celery')
def error_handler(request, exc, traceback):
    print(request)

def simulateing_link():
    result = add.apply_async(
        args=[2,2],
        link=multiply.s(10),
        link_error=error_handler.s()
    )
    print(result.get())
    print(result.children[0].get())
```