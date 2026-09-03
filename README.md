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
| `series: 이름` | `content/posts/<시리즈-슬러그>/` 하위 폴더로 이동 |

## 시리즈(폴더)

노트에 `series: Measure Theory for AI`와 `series_order: 2`를 넣으면 글이
`/posts/measure-theory-for-ai/` 폴더로 들어가고, 폴더 페이지에서 **강 번호순**으로
정렬된다(날짜순 아님). 폴더 자체의 URL은 유지되므로 폴더로 옮기기 전의 평면 URL
(`/posts/<slug>/`)에는 alias가 자동으로 걸린다.

폴더 첫 페이지는 `content/posts/<시리즈-슬러그>/_index.md`이고, 동기화 스크립트는
없을 때만 만들고 이후에는 건드리지 않는다(손으로 쓰는 목차 페이지). `layout: series`가
`layouts/series.html`을 쓰고, frontmatter의 `upcoming` 리스트는 "앞으로 올라올 글"
목록으로 렌더링된다.

## 초기 설정 (최초 1회)

- GitHub에 `heukyoseok-blog` 레포 생성 후 push
- 레포 Settings → Pages → Source를 **GitHub Actions**로 설정
