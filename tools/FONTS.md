# 빌드 폰트

CI·명함 빌더(`build-ci.py`, `build-card.py`)가 글리프를 **아웃라인 패스로 변환**할 때 쓰는 원본이다.
결과물(SVG/PDF)에는 폰트가 아니라 패스만 들어가므로, 배포물에 폰트가 포함되지는 않는다.
그래도 이 저장소는 폰트 파일 자체를 재배포하므로 라이선스 원문을 함께 둔다.

| 파일 | 서체 | 라이선스 | 출처 |
|---|---|---|---|
| `Manrope.ttf` | Manrope (variable, wght) | SIL OFL 1.1 (`Manrope-OFL.txt`) | google/fonts `ofl/manrope` |
| `NotoSansKR.ttf` | Noto Sans KR (variable, wght) | SIL OFL 1.1 (`NotoSansKR-OFL.txt`) | google/fonts `ofl/notosanskr` |

**왜 커밋하는가**: 다른 PC에서 네트워크 없이도 CI 재생성이 재현되어야 한다.
실제로 이 파일들로 재빌드했을 때 이전 빌드의 심볼·파비콘 패스가 **바이트 단위로 동일**함을 확인했다.
폰트 버전이 바뀌면 글리프 아웃라인이 미세하게 달라져 로고가 조용히 변형될 수 있으므로,
버전을 저장소에 고정하는 것이 안전하다.
