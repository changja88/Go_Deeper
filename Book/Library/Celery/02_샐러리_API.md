## Calling API
```python
add.delay(2, 2)
add.apply_async((2, 2))
add.apply_async((2, 2), queue='lopri', countdown=10)
add(2, 2)
```
- apply_async : 테스크 메시지를 보냄 -> AsyncResult를 반환
- delay : apply_async 의 숏컷 -> AsyncResult를 반환
- calling : 함수를 그냥 바로 실행, 워커에게 메시지를 보내지 않고 현재 프로세스 에서 진행

## AsyncResult
```python
res = add.delay(2, 2)
res.get(timeout = 1) # -> 결과를 받는데 1초를 기다린다 (결과값을 뽑는데 1초 준다, 테스크랑은 전혀상관없음) 
res.id
res.failed()
res.successful()
res.state
```