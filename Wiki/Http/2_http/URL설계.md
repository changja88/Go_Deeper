## URL 설계 개념

### 문서(document)

- 단일 개념(파일 하나, 객체 인스턴스, 데이터베이스 row)
- 예) /members/100, files/star.jpg

### 콜렉션(collection)

- 서버가 관리하는 리소스 디렉토리
- 서버가 리소스의 URI를 생성하고 관리
- 예) /members

### 스토어(store)

- 클러이언트가 관리하는 자원 저장소
- 클라이언트가 리소스의 URI를 알고 관리
- 예) /files, 클라이언트가 put으로 전체 경로에 파일을 집어 넣는 경우

### 컨트롤러(controller), 컨트롤 URI

- 문서, 컬렉션, 스토어로 해결하기 어려운 추가 프로세스 실행
- 동사를 직접 사용
- 예) /members/{id}/delete

## PUT, POST 차이점

### PUT

- put으로 들어온 데이터로 서버에 있는 기존 완전히 데이터를 덮는다. 서버에 기존 데이터가 없는 경우 새로 생성한다
    - 서버에 {age:30, gender:male} 인데 put으로 {age:20}을 보내가 되면 서버에서는 gener가 지워지고 {age:20}으로 수정된다
- put은 클라이언트가 서버의 어떤 리소스의 데이터를 수정 할 것인지 알고 있어야 한다
    - PUT | /members/42 &rarr; id42로 member를 생성해줘

### POST

- 사실상 GET, PUT, DELETE, PATCH로 해결할 수 없을 경우 만능으로 사용가능하다
- PUT과 다르게 클라이언트가 서버의 리소르르 특정 하지 않아도 된다
    - POST | /members/ &rarr; id는 서버에서 처리하고 member를 생성해준다

## 기타 주요사항

- POST를 제외한 모든 http mehtod는 멱등해야 한다
    - 여기에서 멱등은 외부에서의 변경은 고려하지 않은, 동일한 요청에 한해서이다
