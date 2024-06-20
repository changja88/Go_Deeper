## 샐러리 - Group Result
```python
job = gourp([
    add.s(2, 2),
    add.s(2, 2),
    add.s(2, 2),
    add.s(2, 2),
])
result = job.apply_async()
result.ready()
result.successful()
result.get()
```