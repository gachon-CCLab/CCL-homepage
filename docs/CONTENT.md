# 내용 보존 기준

- Main → Professor → Cloud Seminar → Members → FedOps → Research → Project → Publication → Gallery → Contact 순서와 Research 하위 2025 / ~ 2024를 유지합니다.
- 현재 멤버 5명과 이전 멤버 15명, 사진·학적·소속·원문 이메일 18개, 구분선·이동 링크를 유지합니다.
- 원본 사진 214회, YouTube 영상 4개와 논문·세미나 자료 링크를 유지합니다.
- 기존 영어 본문과 원문 한국어 고유명사·연락처를 유지합니다.
- 사용자가 선택한 연합학습 그림을 메인과 독립 소개서에 그대로 사용합니다.
- 대학 두 캠퍼스 주소·전화·로고·원래 저작권 문구를 공통 푸터에 보존합니다.
- 이전에 요청받은 Main 환영 제목·그림 교체 기록은 `source/presentation-changes.json`에 보관합니다.

이번 React 전환은 기존 로컬 `ccl-rebuild`의 HTML·CSS·이미지를 활용했습니다. Google Sites 삽입 문서는 사용하지 않았습니다. 전환 전후 본문·이미지·영상·앵커 비교는 `qa/react-preservation.json`, 원문 대조는 `qa/content-report.json`, 실제 화면·동작 검증은 `qa/react-browser-report.json`에 기록합니다.

콘텐츠는 `src/content/`, 레이아웃과 동작은 `src/components/`·`src/features/`·`src/pages/`에서 수정합니다. 변경 뒤 `npm run build`와 `npm run verify:content`로 내용 누락과 링크를 검사하세요.
