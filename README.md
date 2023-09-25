# MultiNewsSummarizer
동국대학교 종합설계_2 공대생의 문단속 - 다중 뉴스 요약 프로그램

## RSS
언론사에서 제공하는 RSS의 뉴스정보를 바탕으로 해당 뉴스기사의 본문을 가져오는 모듈로 NewsData/RSS에 해당 내용이 구현되어 있음

### 사용방법
* NewsData/RSS/newsGenerator를 import
* newsGenerator 모듈로 NewsData/RSS/rssConfig.json에 설정되어 있는 언론사의 뉴스본문을 가져올 수 있으며 매개변수와 사용예제는 아래와 같다.
  * **printOption**: 진행상황의 출력여부, BoolType
  * **skipCondition**: 뉴스기사를 생략하기 위한 조건함수, Bool을 반환하는 Func를 남겨야 함
  * **postProcessFunc**: 가져온 뉴스정보의 후처리를 위한 함수, 반환값은 없다.
```python
newsGenerator.GetNewsArticle_AllMediaCompany(
    printOption=True,skipCondition=None,postProcessFunc=None)
```

### 사용예제
**NewsData/RSS/RSS.py**와 **NewsData/testNewsGenerator.py** 참고
- RSS.py에서 다음과 같은 설정을 사용
  - 진행상황 출력
  - 중복 뉴스 생략
  - 가져온 뉴스본문의 공백제거, html 태그제거, html 엔티티제거
- testNewsGenerator.py는 RSS.py에서 처리한 내용을 `output.json`에 저장
- 실행결과는 **NewsData/RSS/lastPostExample.json**과 **NewsData/RSSOutputExample.json** 참고
