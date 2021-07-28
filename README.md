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

  - Query 클래스에 다양한 메타 데이터를 넣어서, Document 사용자에게 추가적인 
    정보를 줄 수 있다.
    예시:
    - title
    - description
    
  - alias를 통해 외부에 노출하는 API 모양을 바꿀 수도 있다.
  - deprecated 를 추가해 deprecation 여부를 명시할 수 있다.


-  Path Parameters and Numeric Validations
  - Path parameters에는 None 기본값을 넣어도, 여전히 required이다.
  - 파이썬은 기본값이 없는 인자보다 기본값이 있는 인자가 먼저 오면 
    싫어한다. FastAPI는 이름을 통해 인자를 탐지하기 때문에 상관없다.
  - 만약, 순서를 바꾸고 싶다면, 함수의 첫번째 인자를 "\*"로 하면, 
    kwargs로 인자들이 불려지기 괜찮아진다.
  - Path 인자도 Query 인자와 마찬가지로 추가 제약 및 메타 데이터를
    넣을 수 있다.
    - int와 float를 위한:
      - ge(greater than or equal)
      - gt
      - lt
      - le(less than or equal)

    - Query와 Path는 모두 Param 클래스의 서브 클래스이다.
      하지만, 사실 막상 import 되는 Query와 Path는 함수인데,
      동명의 클래스의 인스턴스를 반환한다.
      이렇게 구현된 이유는, 에디터에서 별다른 환경설정 없이
      편하게 쓸 수 있게 하기 위해서다.

      > DX가 정말 중요하게 여겨지기도 하는 구나....

- Body - Multiple parameters
  - 여러 개의 body 인자를 정의하면, 각 인자의 이름을 키로 하는
    객체를 받는 API를 만들 수 있다.
  - 하나의 body 인자만을 받아도, Body 생성자에 "embed=True"를 넣어주면
    인자 이름을 키로 하는 객체를 담은 객체를 body 로 받을 수 있다.
  - Body에도 gt 등의 제약 조건을 넣어줄 수 있다.

- Body - Fields
  - Pydantic의 Field 를 통해 데이터 모델의 각 필드에 대해 메타데이터를 추가하고,
     validation을 정의할 수 있다.
  - Query, Path를 포함해 많은 생성자들은 Param 클래스의 서브 클래스 인스턴스를
    만든다. 그리고 이 Param 클래스는 사실 FieldInfo 클래스의 서브 클래스이다.
  - Field는 FieldInfo 클래스의 인스턴스 또한 반환한다.
  - Body는 FieldInfo 서브 클래스의 인스턴스를 직접 반환한다. 
  - FastAPI 의 많은 함수들(Path, Query, Body, etc)이 특별한 클래스의 생성자를 대신한다.

- Body - Nested Models
  - 커스텀 데이터 모델을 데이터 타입으로 사용해 중첩 모델을 만들 수 있다.
  - Pydantic에서 제공하는 흔히 쓰이는 데이터 모델(예: HttpUrl)을 이용해 
    편하게 더 정교한 데이터 모델을 만들 수 있다.
  - 중첩 모델을 원하는 만큼 깊게 만들 수 있다.

- Declare Request Example Data
  - 커스텀 데이터 모델에 schema_extra 프로퍼티를 가진 Config 서브 클래스를 두면
    JSON Schema가 만들어져 API docs에 예시 모델 같은 추가 정보를 넣을 수 있다.
    // 당연하게도 Pydantic의 기능이다.

  - Body에 example을 넣어도 예시가 생기는데, 이를 이용해서 같은 데이터 모델을
    받는 API라도, 서로 다른 맞춤 예시를 보여줄 수도 있겠다.

  - Body에 examples라는 이름으로 dict을 넘기면 여러 개의 예시를 제공할 수 있다.

  - JSON Schema와 OpenAPI의 표준에 맞추기 위한 몇 가지 기술적인 디테일들이 있다.
    만약 이 예시를 적극적으로 사용할 거라면,
    한 번 쯤은 자세히 스펙을 읽어 볼 필요가 있겠다.

- Extra Data Types
  - int, float, str, bool 과 같은 흔한 데이터 타입 뿐만 아니라,
    다음과 같은 더 복잡한 데이터 타입들도 제공된다:
    - UUID
    - datetime.datetime
    - datetime.date
    - datetime.time
    - datetime.timedelta
    - bytes
    - Decimal

    // 시간과 관련된 타입들은 ISO 8601을 기준으로 한 str이다.
    // 흔히 쓰이는 것들은 그냥 가져다 쓰는 편이 더 좋겠다.
    // Pydantic data types를 살펴보자.

- Cookie Parameters
  - fastapi에서 Cookie 를 불러와 사용하면 된다.
  - Cookie를 사용하지 않으면 쿼리 인자로 해석되기 때문에 명시해줘야 한다.
  - Cookie는 Query와 Path와 형제 클래스로 Param을 부모 클래스로 둔다.

- Header Parameters
  - Cookie Parameters와 설명이 거의 똑같다.
  - 대부분의 표준 헤더는 "-"으로 이어진 문자열이다.
    - 그런데 "user-agent"와 같은 변수명은 파이썬에서 쓸 수 없다.
    - 그래서 Header는 기본적으로 하이픈을 언더스코어(_)로 교체한다.
    - 게다가 HTTP 헤더는 case_insensitive해서 헤더를 파이썬의 표준인 
      snake_case로된 변수들에 담을 수 있다.
    - 언더스코어로의 변환은 옵션을 통해 막을 수 있다.
      - 그런데 HTTP 프록시나 서버들이 언더스코어로 된 헤더를 허용하지
        않을 수도 있다는 걸 염두에 둬야 한다.
  - List[str]로 받으면 동명의 헤더를 여러 개 받을 수 있다.


## doing:
- Reponse Model
