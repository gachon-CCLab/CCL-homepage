# GitHub Pages

- 공개 주소: https://gachon-cclab.github.io/CCL-homepage/
- 배포 소스: `main` 브랜치
- 배포 설정: `.github/workflows/deploy-pages.yml`
- 결과물: `npm run build`가 만든 `dist/` 전체

`main`으로 push하면 Node.js 22에서 의존성 설치·React 빌드·내용 보존 검사를 실행하고, 성공한 결과를 GitHub Pages에 배포합니다. Actions 화면의 `Deploy CCL Homepage`에서 진행 상황을 확인할 수 있습니다. 수동 재배포는 같은 workflow의 `Run workflow`를 사용합니다.

기존 `.html` 주소와 페이지별 자산의 상대 경로를 유지하여 `/CCL-homepage/` 하위에서 동작합니다. 연구실 소개서와 학과 소개도 각각 단일 HTML로 제공됩니다. Google Sites 게시본과는 별도입니다.
