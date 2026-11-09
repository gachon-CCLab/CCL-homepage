# 외부 자료 및 라이선스

## Pretendard

Pretendard 1.3.9 Variable WOFF2를 로컬 파일로 제공합니다. 원본 배포: <https://www.npmjs.com/package/pretendard/v/1.3.9>, 저장소: <https://github.com/orioncactus/pretendard>.

저작권 고지 및 SIL Open Font License 1.1 전문은 `dist/assets/fonts/OFL.txt`에 포함되어 있습니다. 단일 HTML 소개서와 학과 소개 페이지에는 동일한 고지·라이선스 전문을 `script[type="text/plain"]#font-license`로 내장했습니다.

## 기존 CCL 자료

CCL 원문, 인물 사진, 갤러리·세미나 사진, 연구 그림과 프로젝트 자료는 사용자가 제공한 CCL 개편용 자료에서 내용 보존을 위해 가져왔습니다. 원래 기관·저자·출처에 대한 권리를 새로 주장하지 않습니다. `source/asset-map.json`에 원본 이미지 주소와 로컬 파일의 매핑을 보관했습니다.

FedOps 아이콘과 Agent Studio 화면은 제공된 FedOps/CCL 자료입니다. 새로운 연구 분야 개념도는 `dist/assets/research-map.svg`, 파비콘은 `dist/assets/favicon.svg`에 있는 이 작업의 SVG 코드입니다.

메인 우측과 연구실 소개서의 `dist/assets/ccl-hero-ai-data-v2.png`는 내장 image_gen 도구로 편집한 개념적 일러스트입니다. 소개서에는 동일한 이미지 바이트를 내장합니다. 최종 프롬프트는 `source/hero-image-ai-data-v2.md`에 기록했습니다. 기존 형태 `dist/assets/ccl-hero-geometric-v1.png`와 최초 생성 프롬프트 `source/hero-image-prompt.md`도 보관합니다.

## Python 보조 라이브러리

`vendor/pydeps/`의 BeautifulSoup 및 의존성은 개발 시 HTML 재생성·검증에만 사용됩니다. 해당 패키지의 라이선스와 메타데이터를 함께 포함했습니다. 배포용 웹사이트는 이 라이브러리를 사용하지 않습니다.


## React runtime

React, React DOM and Scheduler are distributed under the MIT License. Their notices are included in `public/licenses/` and copied into the built website. Vite, TypeScript and the other development tools retain their licenses through the dependency packages and lockfile.
