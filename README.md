# 흑요석 블로그

Obsidian 볼트(`흑요석`)의 완성된 노트를 Hugo로 공개하는 사이트.

## 글 공개 흐름

1. 볼트 노트 frontmatter에 `publish: true` 추가 (선택: `slug: my-post`, `description: ...`)
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

## 초기 설정 (최초 1회)

- GitHub에 `heukyoseok-blog` 레포 생성 후 push
- 레포 Settings → Pages → Source를 **GitHub Actions**로 설정
