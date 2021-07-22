# Following FastAPI tutorial

link: https://fastapi.tiangolo.com/tutorial/

done:
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



doing:
- Request Body
  - GET에도 request body를 붙일 수 있고, FastAPI에서도 지원한다.
    하지만, 스펙상 정의되지 않아 예상하지 못한 행동을 할 수 있다.
    GET에 body를 붙이는 게 지양돼야 하는 만큼, Swagger UI에서도 
    관련해 문서를 생성하지 않는다. 
    그리고 중간에 있는 프록시들도 GET의 body를 지원하지 않을 수 있다.
   
  

