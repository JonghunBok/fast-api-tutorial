# Following FastAPI tutorial

link: https://fastapi.tiangolo.com/tutorial/

## done:

- First Steps
- Path Parameters

  Enum을 통해 미리 정해진 값을 명시하니 다음이 좋다:
    - 코드에서 허용된 값이 명확하다.
    - 디버깅할 때도, reponse에 가능한 값을 알려줘서 편하겠다.
    - Swagger에서도 가능한 값만 시도해볼 수 있게 해줘서 편하다.

- Query Parameters

  - path 인자로 받지 않은 변수를 path operation function의 인자로 받으면,
    자동으로 query 인자로 해석된다.
  - Optional 타입을 사용하는 건 FastAPI를 위한 게 아니라, 에디터를 위한 것.
    FastAPI는 기본값이 None인 것만으로 해당 변수가 옵셔널인 것을 안다.

    이 말은 곧, Optional이라고 명시해도, None 기본값을 줘야 한다는 뜻이다.
    실제로 None 기본값을 없애니, 해당 쿼리 인자를 반드시 넣어줘야 했다.

  - bool 타입의 query parameter에 모든 스트링이 True인 줄 알았는데,
    그게 아니라 다음의 항목들만 true 값으로 해석된다:

    - 1
    - on
    - yes
    - true
    - True

  - 다중 패쓰 인자와 쿼리 인자의 순서는 중요하지 않다.
    인자들은 이름을 통해 인지된다.

  - 쿼리 인자에 기본값을 주지 않으면, required가 된다.


  > 인자로 받은 변수에 대해서 반드시 적절히 대응해주는 게 인상적이다.
  > 쓰이지 않는 인자를 받을 이유도 없겠지만,
  > 각 인자의 엣지케이스를 잘 처리하고 기본값도 유용하게 만드는 습관을
  > 갖는 게 좋을 것 같다.


- Request Body
  - GET에도 request body를 붙일 수 있고, FastAPI에서도 지원한다.
    하지만, 스펙상 정의되지 않아 예상하지 못한 행동을 할 수 있다.
    GET에 body를 붙이는 게 지양돼야 하는 만큼, Swagger UI에서도 
    관련해 문서를 생성하지 않는다. 
    그리고 중간에 있는 프록시들도 GET의 body를 지원하지 않을 수 있다.
   
  - BaseModel을 상속해 데이터 모델을 만들 때도, path 인자와 같이
    기본값을 이용해 성격을 나타낼 수 있다:
    - 기본값 x: required
    - 기본값 o: not required
    - 기본값 "None": optional
  
  - 데이터 모델을 path operation function에 넣으면,
    fastapi가 알아서 데이터 검증도 해주고, 자세한 에러 메시지도 만든다.
    JSON Schema도 만들고, 그걸 이용해서 documentation UI도 만들어준다.


  - 데이터 모델 대신 dict으로도 받을 수 있지만,
    데이터 모델로 받으면, 데이터 형식이 명확해서 좋다.
    에디터에서도 이걸 이용해 자동완성 및 잘못된 연산을 집어준다.
    이걸 염두에 두고 개발되었다고 한다.

    주류 에디터를 중심으로 DX도 고려하는 프레임워크들이 나오는 요즘,
    vim은 간단한 편집으로만 사용하고, VSCode 같은 툴을
    빨리 익히는 게 좋겠다는 생각이 다시 든다. ㅠㅠ...

  - python에 객체 spread 연산자가 있구나.. (\*\*)

  - 함수 인자들은 다음의 규칙대로 매핑된다:
    - path에도정의되어 있다 -> path parameter
    - singular type 인자다 -> query parameter
    - Pydantic Model 인자다 -> request body


## doing:
- Query Parameters and String Validations
  - Query 클래스를 import해와서 쿼리에 추가적인 제약을 넣을 수 있다.
    예시:
    - min_length
    - max_length
    - regex
      fastapi에서 regex를 곧바로 쓸 수 있다.
  - Query에 기본값을 넣어주면, 이 기본값은 제약사항을 무시한다...
  - Query를 사용하면서, 기본값은 없지만 required 성격을 주고 싶으면, "..."을
    첫번째 인자로 넣으면 된다.
    - 참고: https://docs.python.org/3/library/constants.html#Ellipsis

  - 만약 Query를 이용해 쿼리 인자를 받는다면,
    같은 쿼리 변수를 이용해 리스트를 받을 수도 있다.
    예시: `curl http://localhost:7000/items/\?\q\=123\&q\=124\&q\=-23`
    // 진짜로 해보니 Query 없이는 안된다...
  - Query를 이용해 List에 기본값을 줄 수도 있다.
    하지만 이 때, q를 분기문의 조건으로 두면, 그냥 통과한다.


