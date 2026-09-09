# 흑요석 블로그

Obsidian 볼트(`흑요석`)의 완성된 노트를 Hugo로 공개하는 사이트.

## 글 공개 흐름

1. 볼트 노트 frontmatter에 `publish: true` 추가
   (선택: `slug: my-post`, `description: ...`, `series: ...`, `series_order: 2`)
2. 동기화:
   ```
   python scripts/sync_from_vault.py --vault "C:/Users/user/Documents/git/흑요석"
   ```
3. 로컬 확인: `hugo server` → http://localhost:1313
4. `git add -A && git commit -m "..." && git push` → GitHub Actions가 자동 배포

`publish: true`를 지우고 다시 동기화하면 글이 사이트에서 내려간다.

## 변환 규칙

| 볼트 | 사이트 |
|---|---|
| `[[노트]]` (공개 노트) | 내부 링크 |
| `[[노트]]` (비공개 노트) | 일반 텍스트 |
| `![[이미지.png]]` | `static/images/`로 복사 후 표준 이미지 |
| `> [!note]` 콜아웃 | 일반 인용구 |
| 첫 `# 제목` | 포스트 제목으로 승격(본문에서 제거) |
| `$...$`, `$$...$$` | KaTeX 렌더링 |
| `"인용"` | `“인용”` (곧은 따옴표 → 곱슬 따옴표) |
| `series: 이름` | `content/posts/<시리즈-슬러그>/` 하위 폴더로 이동 |
| `series_index: true` | 글이 아니라 시리즈 폴더 첫 페이지(`_index.md`)로 변환 |

따옴표를 굳이 바꾸는 이유: Hugo의 타이포그래퍼는 닫는 `"` 뒤에 공백이나 구두점이
올 때만 `”`로 바꾼다. 한국어는 조사가 따옴표에 바로 붙어서(`"수렴한다"는`,
`"부피"라고`) 여는 쪽만 `“`가 되고 닫는 쪽은 곧은 따옴표로 남는다. 그래서 동기화
시점에 짝을 지어 미리 바꾼다. **볼트 원본은 곧은 따옴표로 편하게 써도 된다.**
코드·수식 안의 따옴표와 짝이 맞지 않는 줄은 건드리지 않는다(후자는 경고를 낸다).
회귀 테스트: `python scripts/test_curly_quotes.py`

내부 링크(`/posts/...`)와 이미지(`/images/...`)는 루트 상대 경로로 나오는데,
`layouts/_default/_markup/render-link.html`·`render-image.html`이 baseURL의 하위 경로
(GitHub Pages의 `/-heukyoseok-blog/`)를 붙여 준다. 이 훅이 없으면 본문 링크가 깨진다.

## 시리즈(폴더)

노트에 `series: Measure Theory for AI`와 `series_order: 2`를 넣으면 글이
`/posts/measure-theory-for-ai/` 폴더로 들어가고, 폴더 페이지에서 **강 번호순**으로
정렬된다(날짜순 아님). 폴더 자체의 URL은 유지되므로 폴더로 옮기기 전의 평면 URL
(`/posts/<slug>/`)에는 alias가 자동으로 걸린다.

폴더 첫 페이지는 `content/posts/<시리즈-슬러그>/_index.md`이고, 볼트에서 관리한다.
볼트 노트에 `publish: true`, `series_index: true`, `series: 이름`을 넣으면 그 노트가
`_index.md`가 된다(예: `Distillation/Study/Measure Theory for AI/Measure Theory for AI.md`). 목차 노트가 쓰는 frontmatter:

| 키 | 용도 |
|---|---|
| `title` | 페이지 제목 (없으면 본문 첫 `# 제목`, 그것도 없으면 시리즈 이름) |
| `description` | 제목 아래 설명 |
| `summary` | 글 목록 카드 요약 (없으면 `description`) |
| `upcoming_title` | 예고 절 제목 (기본 "앞으로 올라올 글") |
| `upcoming` | 예고 목록 (항목마다 마크다운 허용) |

본문은 글과 같은 규칙으로 변환된다(`[[링크]]`, 수식, 콜아웃). 다른 노트에서 목차 노트로 건
`[[링크]]`는 `/posts/<시리즈-슬러그>/`가 된다. `layout: series`가 `layouts/series.html`을
쓰고, 글 목록은 `series_order` 순으로 정렬된다.

목차 노트가 없는 시리즈 폴더에는 동기화 스크립트가 최소 형태의 `_index.md`를 한 번 만들고
이후 건드리지 않는다(손으로 써도 된다). 목차 노트의 `publish: true`를 지우고 동기화하면
생성됐던 `_index.md`는 삭제되고 같은 실행에서 최소 형태로 다시 만들어진다.

## 초기 설정 (최초 1회)

- GitHub에 `heukyoseok-blog` 레포 생성 후 push
- 레포 Settings → Pages → Source를 **GitHub Actions**로 설정
