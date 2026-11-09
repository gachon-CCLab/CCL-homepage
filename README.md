# CCL Homepage

Cognitive Computing Lab 홈페이지의 **React 19 + TypeScript + Vite** 소스입니다. 기존 로컬 HTML 사이트의 디자인·영문 내용·메뉴·자료를 유지하면서 React 컴포넌트 구조로 전환했습니다. Google Sites 삽입·게시 작업은 별도로 관리합니다.

## 실행

Node.js 22.12 이상을 권장합니다.

```sh
npm ci
npm run dev
```

개발 주소는 `http://127.0.0.1:4333/`입니다. Windows에서는 `Start-dev.cmd`를 실행할 수도 있습니다.

```sh
npm run build          # TypeScript 검사 + React 정적 출력
npm run preview        # 빌드 결과 확인
npm run verify:content # 원본 본문·사진·영상·메뉴·링크 검사 (Python)
npm run package        # 배포용 releases/ccl-website.zip 생성 (Python)
```

빌드에는 Node.js만 필요합니다. 내용 검사·ZIP 도구는 Python 3.10 이상을 사용하며, 필요한 기존 파서 라이브러리는 `vendor/pydeps/`에 포함돼 있습니다.

## 폴더 구조

```text
src/
  app/                 페이지 URL과 지연 로딩
  components/
    layout/            공통 헤더·푸터·레이아웃
    content/           페이지 제목·문서·구조화된 본문 렌더러
    media/             React 사진 뷰어와 사진 링크
  features/
    home/              메인 Hero
    members/           멤버 카드·현재/이전 그룹
    seminars/          세미나 카드
  pages/               11개 페이지 진입점
  content/             본문·메뉴·멤버·세미나 데이터
  styles/              기본·레이아웃·메인·문서·뷰어·반응형 CSS
scripts/               React 정적 출력·독립 소개서 생성
public/assets/         이미지·폰트 원본
public/licenses/       배포 라이선스 고지
source/                원문 보존 검사에 사용하는 이전 내용·자료
source/raw/            원본 HTML 스냅샷
templates/            단일 파일 소개서 2개의 원본 템플릿
tools/                내용 검사·배포 ZIP 도구
qa/                   React 전환 전후 대조·화면 검증
legacy/               이전 Python 생성기와 일회성 이전 도구
dist/                 생성된 배포 결과 (Git 제외)
releases/             배포 ZIP (Git 제외)
```

## 수정할 곳

| 작업 | 위치 |
| --- | --- |
| 헤더·내비게이션 | `src/components/layout/Header.tsx`, `src/content/navigation.json` |
| 공통 푸터 | `src/components/layout/Footer.tsx`, `src/content/footer.json` |
| 메인 첫 화면 | `src/features/home/Hero.tsx` |
| 메인 소개·FedOps·선정 논문·연구실 생활 | `src/content/pages/main.json` |
| 현재·이전 멤버 | `src/content/members.json` |
| 멤버 카드와 구분선 | `src/features/members/`, `src/pages/members.tsx` |
| 세미나 | `src/content/seminars.json`, `src/features/seminars/` |
| 연구·논문·과제·갤러리 원문 | 해당 `src/content/pages/*.json` |
| 사진 확대·키보드 탐색 | `src/components/media/PhotoViewer.tsx` |
| 색·간격·반응형 | `src/styles/` |
| 연구실 소개서·학과 소개 | `templates/ccl-introduction.html`, `templates/department.html` |

## 배포 결과

`npm run build`는 React에서 본문을 미리 렌더링한 **11개 HTML 페이지**를 만들고, 브라우저에서는 같은 React 트리를 연결해 메뉴와 사진 뷰어를 동작시킵니다. 페이지별 코드·데이터는 분리해서 로드합니다. 웹 서버에 `dist/` 전체를 올리면 되며 별도 Python·Node 서버는 필요하지 않습니다.

기존 `index.html`, `members.html`, `research-2025.html` 등의 URL과 문서 앵커를 유지합니다. `ccl-introduction.html`과 `department.html`은 이미지·폰트·스타일을 내장한 **각각 HTML 파일 하나**로 계속 제공됩니다. 영상 및 React 상호작용은 HTTP 미리보기로 확인하세요.

현재 멤버 5명·이전 멤버 15명, 구분선·상단 바로가기, 원본 사진·영상·자료 링크, 기존 영문 내용을 유지했습니다. 전환 전후 13개 문서의 본문·이미지·영상·앵커 일치 결과는 `qa/react-preservation.json`에 기록합니다.

구조 설명은 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), 내용 보존 기준은 [docs/CONTENT.md](docs/CONTENT.md), 라이선스는 [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md)를 참고하세요.
