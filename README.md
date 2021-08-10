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

- Reponse Model
  - 요청으로 들어오는 데이터를 위한 모델 뿐만 아니라,
    응답으로 보내는 데이터를 위한 데이터 모델도 정의할 수 있다.
  - 데코레이터 함수에 response_model이라는 이름의 인자를 주면 된다.
  - 이렇게 하면 내가 정확한 형식으로 응답을 보내고 있는지 확인할 수 있다.
  - fastapi는 response_model을 가지고 다음을 한다:
    - 타입 정의에 맞게 출력 데이터를 변환
    - 데이터 검증
    - 응답을 위한 JSON Schema 추가
    - 자동 문서화에 사용
    - 모델에 맞게 출력 데이터 제한 **(가장 중요하다)**
      > 필터가 되는게 정말 방어적인 프로그래밍을 할 때 편할 것 같다.
  - 응답에도 기본값을 넣을 수 있다.
    - "response_model_exclude_unset" 플래그를 참으로 하면,
      필드에 기본값이 있어도 초기화되지 않았다면 응답에 포함시키지 않을 수 있다.
    - 기본값과 같은 값이라도 명시적으로 대입됐다면, 응답에  포함된다.
  - response_model_include, response_model_exclude 를 통해 어떤 필드만 응답에 포함할지, 안할지 정할 수 있다.

- Extra Models
    > 이를 통해 같은 데이터 모델을 쓰면서도 실제 응답의 형태를 조정할 수 있겠다.
  - 고차원 모델을 만듦으로써 코드의 중복을 피할 수 있다.
    - 이 때 다양한 자식 클래스들을 일종의 "state"로 생각할 수도 있다.
  - 타입에 Union도 사용할 수 있다...
    > typing을 파이썬에서 typescript를 사용하게 해주는 라이브러리로 이해해도 문제없겠다...


- Response Status Code
  - 데코레이터 함수 안에 status_code 정수 인자를 넣어 응답의 상태 코드를 명시할 수 있다.
  - fastapi에서 status를 import해 사용해도 된다.
    - starlette에서 가져와도 된다. 
    - 똑같은 status고, 편의를 위해 fastapi에서도 제공하는 거다.
  - 상태 코드별 특성도 FastAPI가 이해해서 알아서 문서를 알맞게 만들어 준다.
    - 특정 상태 코드는 body가 없는 응답이라던지 등등

- Form Data
  - Form 은 Body를 직접 상속한다.
  - **percent encoding**

- Request Files
  - Form도 그렇고, UploadFile도 그렇고, 업로드되는 파일을 받거나 폼을 사용하려면
    python-mulitpart를 설치하라고 한다.
    > 없어도 되긴 예제가 잘 돌아가긴 한다. 
    > 아마 fastapi를 full로 설치할 때 같이 들어오거나,
    > 서버에서 가공할 때 문제가 생기나 보다.
    > form에서 데이터를 submit할 때 multipart로 간다고 한다.
  - File은 Form 클래스를 직접 상속한다.
  - File을 사용하지 않으면 body나 query 인자로 해석하기 때뭉네 꼭 붙여야 한다.
  - bytes로 파일을  받으면, FastAPI가 파일을 읽어서 그 내용을 bytes에 담는다.
    - 이 말은 파일 전체가 메모리에 담긴다는 뜻이다.
    > 스케일이 커지면 바로 문제가 생길 듯...
  - UploadFile을 사용하면 다음의 장점이 있다:
    - spooled file을 이용한다.
      - 특정 용량까지는 메모리에 차지만, 그 이상으로는 디스크에 저장되는 방식
    - 메모리를 바닥내지 않으면서 큰 파일을 다룰 수 있다:
      - image
      - video
      - large binaries
      - etc
    - 업로드된 파일의 메타데이터를 얻을 수 있다.
    - file-like한 async 인터페이스를 갖고 있다.
    - UploadFile은 다음의 속성을 갖는다:
      - filename: str, 원래 파일의 이름
      - content_type: str, MIME type/media type
      - file: SpooledTemporaryFile
    - UploadFile은 다음의 async 메소드를 갖는다:
      - write(data)
      - read(size)
      - seek(offset)
      - close()
  - File도 List를 붙여 여러 개를 한 번에 받을 수 있다.

- Request Forms and Files
  - Form과 File, UploadFile을 함께 써서 동시에 받을 수도 있다.

- Handling Errors
  - HTTPException을 이용해 클라이언트에게 의미있는
    에러 메시지를 전달할 수 있다.
  > python은 throw가 아니라 raise구나...
  - 커스텀 에러도 넣을 수 있다..
    - starlette의 exception utilites를 사용할 수 있다.
  - detail 인자에는 str 뿐만 아니라 JSON화 할 수 있는 데이터는 다 넣을 수 있다.
  - error 발생 시에는 응답이 미들웨어를 거치지 못한다..
    - 요청은 거치는데, 중간에 흐름이 끊긴다.
  - FastAPI는 default exception handler를 제공하고, 이 핸들러들은 오버라이드할
    수 있다:
    - RequestValidationError
    - ValidationError
    - HTTPException error handler
  - 오버라이드 뿐만 아니라 재사용도 할 수 있다.
    - 기본 핸들러를 호출하는 상위 함수를 만들어서!

- Path Operation Configuration
  - path operation decorator에 인자를 넘겨 오퍼레이션을 설정할 수 있다.
  - status_code
  - tags
  - summary
  - description
  - docstring (인자에 넣는 건 아니다. 함수 시그니쳐 바로 아래)
  - response_description
  - deprecated

- JSON Compatible Encoder
  - fastapi는 jsonable_encoder를 제공한다.
    - 이 엔코더를 이용해 Pydantic model처럼 JSON 호환 형식으로 
      변환해야 하는 데이터를 변환할 수 있다.
    - 데이터베이스에 데이터를 넣을 때 사용할 수 있다.
    - 파이썬 스탠다드 json.dumps()와 비슷하다.

- Body - Updates
  - 원래 부분 업데이트는 PUT이 아니라 PATCH를 쓴다고 한다.
    - 근데 그냥 PUT을 쓰곤 한다.
    - FastAPI가 하나의 방식을 강제하진 않는다.
  - 부분 업데이트는 추가적인 노력이 들어가고, FastAPI는
    필요한 메소드를 제공한다.

- Dependencies
  - Dependencies - First Steps
    - FastAPI는 강력하고 직관적인 DI(Dependency Injection) 시스템을 가진다.
    - DI는 다음의 상황에서 유용할 수 있다:
      - 공통 로직이 있을 때
      - DB 커넥션을 공유할 때
      - security, authentication, role requirements, etc를 강제할 때
    - DI의 다른 이름들:
      - resources
      - providers
      - services
      - injectables
      - components
  - Classes as Dependencies
    - Dependency의 반환값을 그저 dict로 받으면, 에디터는 반환값의 형식을 모른다.
    - Dependency는 꼭 함수일 필요는 없고, "callable"하기만 하면 된다.
      - 파이썬에서 Class는 callable이다.
      - 그래서 FastAPI에서는 파이썬 클래스를 dependency로 사용할 수 있다.
      - 만약 클래스를 사용하고 있다면 Type Annotation이나 Depends의 인자 중 하나를
        생략할 수 있다.
        - Type Annotation을 생략하면 에디터의 도움을 못받는다.
        - Depends의 인자를 생략하면, 코드가 헷갈릴 수 있지만, 코드 중복을 피할 수 있다.

  - Sub-dependencies
    - 디펜던시 트리는 원하는 만큼 깊어질 수 있다.
    - 디펜던시가 "디펜던시"이면서 동시에 "디펜더블"일 수 있다.
    - 다수의 디펜던시가 같은 sub-dependency를 가져도, FastAPI가 알아서 한 번만 호출한다.
  - Dependencies in path operation decorators
    - 함수가 아니라 데코레이터에 디펜던시를 넣을 수도 있다.
      - 이땐 dependencies라는 인자에 Depends()의 리스트를 넣으면 된다.
  - Global Dependencies
    - 아예 dependencies를 FastAPI의 인스턴스를 만들 때 넣어주면,
      글로벌하게 디펜던시를 적용할 수 있다.
  - Dependencies with yield
    - 요청 처리를 마친 후에 디펜던시의 남은 코드를 실행할 수도 있다.
      - exit, cleanup, teardown, close, context managers 등으로 불리는 작업들.
    - 이때는 return 대신 yield를 사용한다.
      - yield는 한 번만 사용한다.
    - Python 3.7 이상을 사용하거나, Python 3.6에 "backports"를 설치해야 한다.
    - 내부적으로 Python의 Context Managers를 사용한다.
    - yield 이후의 작업은 이미 응답이 보내진 후에 작동한다.
      - HTTPException 에러를 내려면 Exception Handler를 작성해야 한다.
      - 그래서 db 연결이 응답 전까지 유지되고,
        디펜던시 사이에 공유될 수 있다.
    - Context Managers는 with과 함께 쓸 수 있는 파이썬 오브젝트다.

- Security
  - OAuth2에는 여러 "flows"가 있다.
  - 본 튜토리얼에서는 `password` flow를 이용한다.
  - JWT도 맛을 본다.
  - OAuth2 스펙과 JWT에 대한 이해 없이는 별 의미가 없겠다 싶어 따라만 해보았다.
  - 스펙 공부의 중요성을 알게 됐다.


  - Get Current User
  - Smaple OAuth2 with Password and Bearer
  - OAuth2 with Password (and hashing), Bearer with JWT tokens

- Middelware
  - 콜백함수와 비슷한 흐름제어가 있는 듯 하다.
  - 모든 요청과 응답이 거치는 곳이라고 생각하면 된다.

- CORS(Cross-OriginResource Sharing)
  - origin은 다음의 조합이다:
    - protocol (http, https)
    - domain
    - port
  > 당연히도 CORS는 L7... 브라우저에서 검사하니깐..

  - allowed origins를 와일드카드(*)로 둘 수도 있다.
    그런데 그러면, credential과 관련된 통신은 허용되지 않는다:
    - Cookies
    - Authorization headers
      - Bearer Tokens
      - etc
  - FastAPI는 CORSMiddleware를 제공한다.
  - CORSMiddleware는 다음의 인자를 받을 수 있다:
    - allow_origins
    - allow_origin_regex
    - allow_methods
    - allow_headers
    - allow_credentials
    - expose_headers
    - max_age

- SQL (Relational) Databases
  - 그저 따라하기만 될 것 같아 생략한다.

- Bigger Applications - Mulitple Files
  - APIRouter를 이용해 작은 app인 router들을 만들 수 있다.
  - `__init__.py`를 이용해 패키지화해서 import를 편하게 하는 게 폴더 구조 구성의 핵심이다.

- Background Tasks 
  - 응답을 보낸 후에 어떤 작업들을 할지 예약할 수 있다.
  - 굳이 유저가 기다릴 필요가 없는 일들을 이렇게 처리하면 된다.
  - background task는 async일 수도 있고, 아닐 수도 있다.
  - background_tasks라는 BackgroundTasks 타입의 인자를 받고,
    이 객체의 .add_task() 함수를 이용하면 된다.
  - 디펜던시 안에서도 잘 작동한다.
  - starlette의 starlette.background에서 그대로 가져왔다.
  - 만약 추가적으로 실행하는 백그라운드 테스트가 무겁고,
    같은 프로세스에서 처리할 필요가 없다면, Celery, RabbitMQ,
    Redis 같은 더 큰 전문적 툴을 이용하는 것을 고려해 볼 수 있다.

- Metadata and Docs URLs
  - FastAPI를 처음 초기화할 때 인자를 넣어 앱에 대한 메타데이터를
    설정할 수 있다.
    - title
    - description
    - version
    - terms_of_service: URL이어야 한다.
    - contact
    - license_info
    - openapi_tags
    - openapi_url
    - docs_url


- Static Files
  - StaticFiles를 사용해 디렉토리로부터 정적파일을 서빙할 수 있다.
  - aiofiles라는 라이브러리를 설치해야 한다.
  - sub-path를 담당하며, 정적 파일을 다루는 독립적인 application을
    만들고 마운팅 시키는 식이다. 3가지 정보가 필요하다:
    - sub-path
    - directory name
    - 내부적으로 사용될 이름

- Testing
  - Python의 Requests에 기반하여 친숙하고 직관적이다.
    - 구글링하기도 쉽다.
    - 만약 fastapi로 TDD하게 되면, Request 문서를
      일독하고 해야 하겠다.
  - Starlette 덕분에 테스팅이 쉽고 재밌다.
  - pytest를 직접적으로 이용할 수 있다.
  > 상대 주소를 사용하려면, __init__.py를 만들어 패키지로
    만들어줘야 한다...
  > pytest가 직관적이라 편하다.


- Debugging
  - IDE를 이용해 디버깅하려면, 서버 파일이 메인으로서 실행돼야 한다.
    - if __name__ == "__main__": 아래에서 직접 uvicorn을 실행한다.
    - 그리고 IDE의 디버깅 기능을 이용하면 된다.

---

> 전반적으로 Starlette, Pydantic의 문서까지 봐야 
> 이해하고 파인 튜닝할 수 있는 부분들이 있다.
> 편하긴 하지만, 그렇다고 기반 기술을 아주 모르고 
> 사용할 순 없겠다.
> 모든 hihg-level tool들의 숙명인 것 같다.
> 덜 생각하며 쓰려고 만들었지만, 결국 모든 걸 생각해야 하는.. ㅠㅠ..
