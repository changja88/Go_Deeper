## 샐러리 - retry
```python
@app.task(bind=True) 
def send_twitter_status(self,  oauth, tweet):
    try:
        twitter = Twitter(oauth)
        twitter.update_status(tweet)
    except:
        raise self.retry(exc=exc)
```
- bind를 하면 self를 쓸 수 있다

```python
@app.task(bind=True, default_retry_delay= 30 * 60)  # 30분 후에 시도
def send_twitter_status(self,  oauth, tweet):
    try:
        twitter = Twitter(oauth)
        twitter.update_status(tweet)
    except:
        raise self.retry(exc=exc, countdown=60) # 위에서 30분으로 헀지만 1분으로 바꿀수 있다
```

```python
from twitter.exceptions import FailWhaleError


@app.task(autoretry_for=(FailWhaleError,))
def refresh_timeline(user):
    return twitter.refresh_timeline(user)
```
- FailWhaleError 에러가 발생 했을 때만 재시도

```python
from twitter.exceptions import FailWhaleError


@app.task(autoretry_for=(FailWhaleError,), retry_kwargs={'mas_retries':5})
def refresh_timeline(user):
    return twitter.refresh_timeline(user)
```
- FailWhaleError 에러가 발생 했을 때만 재시도
- 5번만 재시도하고 그 이후에도 발생하면 에러 발생