#!/usr/bin/env python3
"""Obsidian 볼트에서 `publish: true` 노트만 Hugo 포스트로 동기화한다.

사용법:
    python scripts/sync_from_vault.py --vault "C:/Users/user/Documents/git/흑요석"

동작:
  1. 볼트의 모든 .md 중 frontmatter에 `publish: true`가 있는 노트만 고른다.
  2. [[위키링크]] → 대상도 공개 노트면 내부 링크, 아니면 일반 텍스트로 바꾼다.
  3. ![[이미지]] 임베드 → static/images/ 로 복사하고 표준 마크다운 이미지로 바꾼다.
  4. Obsidian 콜아웃(> [!note]) 마커를 제거해 일반 인용구로 만든다.
  5. content/posts/<slug>.md 로 쓰고, 더 이상 publish 가 아닌 글은 삭제한다(미러링).

의존성: 표준 라이브러리만 사용.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

SKIP_DIRS = {".obsidian", ".trash", ".git", "templates", "Templates"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
MARKER = "vault_source"  # 이 스크립트가 만든 포스트임을 표시하는 frontmatter 키

FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
WIKILINK_RE = re.compile(r"(!?)\[\[([^\]|#]+)(?:#([^\]|]+))?(?:\|([^\]]+))?\]\]")
CALLOUT_RE = re.compile(r"^(>\s*)\[!\w+\][+-]?[ \t]*(.*)$", re.MULTILINE)
H1_RE = re.compile(r"^#\s+(.+?)\s*$")


def extract_leading_title(body: str) -> tuple[str | None, str]:
    """본문의 첫 non-empty 줄이 H1이면 그것을 제목으로 떼어낸다.

    노트 중간에 나오는 `# 요약`, `# 1. ...` 같은 섹션 헤딩까지 제목으로
    오인하지 않도록, 첫 줄일 때만 승격한다.
    """
    lines = body.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        m = H1_RE.match(line)
        if m:
            return m.group(1).strip(), "".join(lines[:i] + lines[i + 1:])
        break
    return None, body


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """최소 YAML 파서: 스칼라와 `- item` 리스트만 처리한다."""
    m = FM_RE.match(text)
    if not m:
        return {}, text
    fm: dict = {}
    key = None
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        if line.startswith((" ", "\t")) and line.strip().startswith("- ") and key:
            fm.setdefault(key, []).append(_unquote(line.strip()[2:]))
        elif ":" in line and not line.startswith((" ", "\t")):
            key, _, val = line.partition(":")
            key, val = key.strip(), val.strip()
            fm[key] = _unquote(val) if val else []
    return fm, text[m.end():]


def _unquote(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def is_truthy(v) -> bool:
    return str(v).strip().lower() in {"true", "yes", "1"}


def slugify(name: str) -> str:
    s = re.sub(r"[^\w\s-]", "", name, flags=re.UNICODE).strip()
    return re.sub(r"[\s_]+", "-", s).lower()


def collect_notes(vault: Path) -> dict[str, Path]:
    """노트 이름(stem) → 경로. 위키링크 해석용."""
    notes: dict[str, Path] = {}
    for p in vault.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.relative_to(vault).parts):
            continue
        notes.setdefault(p.stem, p)
    return notes


def find_asset(vault: Path, name: str) -> Path | None:
    for p in vault.rglob(name):
        if p.is_file():
            return p
    return None


def convert_body(
    body: str, vault: Path, published: dict[str, str], static_img: Path
) -> str:
    def repl(m: re.Match) -> str:
        embed, target, heading, alias = m.group(1), m.group(2).strip(), m.group(3), m.group(4)
        if embed:
            suffix = Path(target).suffix.lower()
            if suffix in IMAGE_EXTS:
                src = find_asset(vault, target)
                if src:
                    static_img.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, static_img / src.name)
                    return f"![{alias or ''}](/images/{src.name})"
                print(f"  [warn] 이미지 없음: {target}", file=sys.stderr)
                return ""
            # 노트 임베드는 지원하지 않음 → 링크로 강등
        label = alias or (f"{target} › {heading}" if heading else target)
        if target in published:
            anchor = f"#{slugify(heading)}" if heading else ""
            return f"[{label}](/posts/{published[target]}/{anchor})"
        return label

    body = WIKILINK_RE.sub(repl, body)
    body = CALLOUT_RE.sub(
        lambda m: f"{m.group(1)}**{m.group(2).strip()}**" if m.group(2).strip() else m.group(1).rstrip(),
        body,
    )
    return body.strip() + "\n"


def build_frontmatter(title: str, fm: dict, rel_path: str) -> str:
    today = date.today().isoformat()
    created = str(fm.get("creation_date") or today)
    tags = fm.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]
    lines = [
        "---",
        f'title: "{title.replace(chr(34), chr(39))}"',
        f"date: {created}",
        f"lastmod: {today}",
        "draft: false",
        "math: true",
    ]
    if tags:
        lines.append("tags:")
        lines += [f'  - "{t}"' for t in tags]
    if fm.get("description"):
        lines.append(f'description: "{fm["description"]}"')
    lines.append(f'{MARKER}: "{rel_path}"')
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def main() -> int:
    for stream in (sys.stdout, sys.stderr):  # Windows 콘솔에서 한글 깨짐 방지
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True, type=Path)
    ap.add_argument("--site", default=Path(__file__).resolve().parent.parent, type=Path)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    vault: Path = args.vault.resolve()
    posts_dir: Path = args.site / "content" / "posts"
    static_img: Path = args.site / "static" / "images"
    posts_dir.mkdir(parents=True, exist_ok=True)

    all_notes = collect_notes(vault)

    # 1) 공개 대상 선별
    to_publish: list[tuple[Path, dict, str]] = []
    for stem, path in all_notes.items():
        text = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if is_truthy(fm.get("publish", "")):
            to_publish.append((path, fm, body))

    published: dict[str, str] = {
        p.stem: str(fm.get("slug") or slugify(p.stem)) for p, fm, _ in to_publish
    }

    # 2) 변환 및 쓰기
    written: set[str] = set()
    for path, fm, body in to_publish:
        slug = published[path.stem]
        leading_title, stripped_body = extract_leading_title(body)
        if fm.get("title"):
            title = str(fm["title"])  # 본문은 그대로 둔다 (첫 H1이 실제 섹션 제목일 수 있음)
        elif leading_title:
            title = leading_title
            body = stripped_body
        else:
            title = path.stem
        rel = path.relative_to(vault).as_posix()
        out = build_frontmatter(title, fm, rel) + convert_body(body, vault, published, static_img)
        dest = posts_dir / f"{slug}.md"
        written.add(dest.name)
        if args.dry_run:
            print(f"[dry] {rel} -> {dest.relative_to(args.site)}")
        else:
            dest.write_text(out, encoding="utf-8", newline="\n")
            print(f"[ok]  {rel} -> {dest.relative_to(args.site)}")

    # 3) 더 이상 publish 가 아닌 글 제거 (이 스크립트가 만든 것만)
    for existing in posts_dir.glob("*.md"):
        if existing.name in written:
            continue
        if MARKER in existing.read_text(encoding="utf-8")[:2000]:
            if args.dry_run:
                print(f"[dry] remove {existing.name}")
            else:
                existing.unlink()
                print(f"[rm]  {existing.name}")

    print(f"\n{len(written)}개 글 동기화 완료.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
