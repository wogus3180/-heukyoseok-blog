#!/usr/bin/env python3
"""Obsidian 볼트에서 `publish: true` 노트만 Hugo 포스트로 동기화한다.

사용법:
    python scripts/sync_from_vault.py --vault "C:/Users/user/Documents/git/흑요석"

동작:
  1. 볼트의 모든 .md 중 frontmatter에 `publish: true`가 있는 노트만 고른다.
  2. [[위키링크]] → 대상도 공개 노트면 내부 링크, 아니면 일반 텍스트로 바꾼다.
  3. ![[이미지]] 임베드 → static/images/ 로 복사하고 표준 마크다운 이미지로 바꾼다.
  4. Obsidian 콜아웃(> [!note]) 마커를 제거해 일반 인용구로 만든다.
  5. `series: 이름`이 있으면 content/posts/<시리즈-슬러그>/<slug>.md, 없으면
     content/posts/<slug>.md 로 쓰고, 더 이상 publish 가 아닌 글은 삭제한다(미러링).
  6. `series_index: true` 노트는 글이 아니라 시리즈 폴더의 목차 페이지
     (content/posts/<시리즈-슬러그>/_index.md)가 된다. 그런 노트가 없는 시리즈
     폴더에는 최소 형태의 _index.md 를 만들어 두고 이후 건드리지 않는다.

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

# 수식 안의 `=` 나 `-` 단독 줄은 CommonMark가 Setext 제목 밑줄로 오인해서
# 수식을 통째로 망가뜨린다 (예: "\mathcal P(\Omega)\n=\n\{...\}"). 이스케이프된
# `\{`, `\{` 도 일반 텍스트로 들어가면 백슬래시 이스케이프 규칙에 걸려 사라진다.
# 그래서 수식은 마크다운이 절대 손대지 않는 코드펜스/코드스팬으로 감싸서
# 원본 그대로 보존한 뒤, 클라이언트에서 KaTeX가 그 텍스트를 직접 렌더링한다.
BLOCK_MATH_RE = re.compile(r"\$\$(.*?)\$\$|\\\[(.*?)\\\]", re.DOTALL)
INLINE_MATH_RE = re.compile(r"\$([^\$\n]+?)\$|\\\((.*?)\\\)")


def protect_math(body: str) -> str:
    def block_repl(m: re.Match) -> str:
        content = (m.group(1) if m.group(1) is not None else m.group(2)).strip("\n")
        return f"\n```math\n{content}\n```\n"

    def inline_repl(m: re.Match) -> str:
        content = (m.group(1) if m.group(1) is not None else m.group(2)).replace("`", "")
        return f"`\\({content}\\)`"

    body = BLOCK_MATH_RE.sub(block_repl, body)
    return INLINE_MATH_RE.sub(inline_repl, body)


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
    body = protect_math(body)

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


def build_frontmatter(title: str, fm: dict, rel_path: str, slug: str) -> str:
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
    # description 은 글 제목 바로 아래에 그대로 노출되고, summary 는 목록 카드에
    # 쓰인다. summary 가 없으면 목록 카드가 본문 첫 문단(=보호된 LaTeX 원문)을
    # 그대로 보여주므로 description 으로 채운다. 제목 아래는 짧게, 목록은 길게
    # 가고 싶으면 노트에서 summary 를 따로 준다.
    desc = str(fm.get("description") or "").strip()
    summary = str(fm.get("summary") or desc).strip()
    if desc:
        lines.append(f"description: {yaml_quote(desc)}")
    if summary:
        lines.append(f"summary: {yaml_quote(summary)}")
    series = str(fm.get("series") or "").strip()
    if series:
        lines.append(f'series: "{series}"')
        order = str(fm.get("series_order") or "").strip()
        if order:
            lines.append(f"series_order: {order}")
        # 시리즈 폴더로 옮기기 전의 평면 URL(/posts/<slug>/)로 들어오던 링크를 살려둔다.
        lines.append("aliases:")
        lines.append(f'  - "/posts/{slug}/"')
    lines.append(f'{MARKER}: "{rel_path}"')
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def resolve_title(fm: dict, body: str, fallback: str) -> tuple[str, str]:
    """frontmatter title > 본문 첫 H1(본문에서 제거) > fallback 순으로 제목을 정한다."""
    if fm.get("title"):
        return str(fm["title"]), body  # 본문은 그대로 둔다 (첫 H1이 실제 섹션 제목일 수 있음)
    leading_title, stripped = extract_leading_title(body)
    if leading_title:
        return leading_title, stripped
    return fallback, body


def yaml_quote(s) -> str:
    """YAML 큰따옴표 문자열. 안에 든 따옴표/백슬래시를 이스케이프한다."""
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_index_frontmatter(title: str, fm: dict, rel_path: str) -> str:
    """`series_index: true` 노트 → 시리즈 폴더 첫 페이지(_index.md)의 frontmatter.

    layouts/series.html 이 읽는 필드: title, description, upcoming_title, upcoming.
    summary 는 홈 목록 카드용이며 없으면 description 을 쓴다.
    """
    lines = [
        "---",
        f"title: {yaml_quote(title)}",
        'layout: "series"',
        "ShowToc: false",
        f"{MARKER}: {yaml_quote(rel_path)}",
    ]
    desc = str(fm.get("description") or "").strip()
    summary = str(fm.get("summary") or desc).strip()
    if desc:
        lines.append(f"description: {yaml_quote(desc)}")
    if summary:
        lines.append(f"summary: {yaml_quote(summary)}")
    if fm.get("upcoming_title"):
        lines.append(f"upcoming_title: {yaml_quote(fm['upcoming_title'])}")
    upcoming = fm.get("upcoming") or []
    if isinstance(upcoming, str):
        upcoming = [upcoming]
    if upcoming:
        lines.append("upcoming:")
        lines += [f"  - {yaml_quote(u)}" for u in upcoming]
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def series_index_stub(name: str) -> str:
    return f'---\ntitle: "{name}"\nlayout: "series"\n---\n'


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

    # 1) 공개 대상 선별. `series_index: true` 노트는 글이 아니라 시리즈 폴더의 목차 페이지다.
    to_publish: list[tuple[Path, dict, str]] = []
    index_notes: list[tuple[Path, dict, str]] = []
    for stem, path in all_notes.items():
        text = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        if not is_truthy(fm.get("publish", "")):
            continue
        if is_truthy(fm.get("series_index", "")):
            if not str(fm.get("series") or "").strip():
                print(f"  [warn] series_index 노트에 series 가 없어 건너뜀: {path.name}", file=sys.stderr)
                continue
            index_notes.append((path, fm, body))
        else:
            to_publish.append((path, fm, body))

    # 노트 이름 → (슬러그, posts/ 기준 상대경로). 시리즈가 있으면 하위 폴더로 들어간다.
    routes: dict[str, tuple[str, str]] = {}
    for p, fm, _ in to_publish:
        slug = str(fm.get("slug") or slugify(p.stem))
        series = str(fm.get("series") or "").strip()
        routes[p.stem] = (slug, f"{slugify(series)}/{slug}" if series else slug)
    published: dict[str, str] = {stem: rel for stem, (_, rel) in routes.items()}
    # 목차 노트로 가는 [[링크]]는 시리즈 폴더 URL(/posts/<시리즈-슬러그>/)이 된다.
    for p, fm, _ in index_notes:
        published[p.stem] = slugify(str(fm["series"]).strip())

    # 2) 글 변환 및 쓰기
    written: set[str] = set()
    series_dirs: dict[str, str] = {}  # 폴더 슬러그 → 시리즈 표시 이름
    for path, fm, body in to_publish:
        slug, route = routes[path.stem]
        title, body = resolve_title(fm, body, path.stem)
        rel = path.relative_to(vault).as_posix()
        out = build_frontmatter(title, fm, rel, slug) + convert_body(
            body, vault, published, static_img
        )
        dest = posts_dir / f"{route}.md"
        written.add(f"{route}.md")
        if "/" in route:
            series_dirs[route.split("/")[0]] = str(fm.get("series")).strip()
        if args.dry_run:
            print(f"[dry] {rel} -> {dest.relative_to(args.site)}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(out, encoding="utf-8", newline="\n")
            print(f"[ok]  {rel} -> {dest.relative_to(args.site)}")

    # 3) 시리즈 목차 페이지: 볼트의 `series_index: true` 노트로 _index.md 를 만든다.
    index_written: set[str] = set()
    for path, fm, body in index_notes:
        series = str(fm["series"]).strip()
        dir_slug = slugify(series)
        title, body = resolve_title(fm, body, series)
        rel = path.relative_to(vault).as_posix()
        if dir_slug in index_written:
            print(f"  [warn] 시리즈 '{series}' 목차 노트가 둘 이상, {rel} 로 덮어씀", file=sys.stderr)
        out = build_index_frontmatter(title, fm, rel) + convert_body(
            body, vault, published, static_img
        )
        dest = posts_dir / dir_slug / "_index.md"
        written.add(f"{dir_slug}/_index.md")
        index_written.add(dir_slug)
        series_dirs.setdefault(dir_slug, series)
        if args.dry_run:
            print(f"[dry] {rel} -> {dest.relative_to(args.site)}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(out, encoding="utf-8", newline="\n")
            print(f"[ok]  {rel} -> {dest.relative_to(args.site)}")

    # 4) 더 이상 publish 가 아닌 글·목차 제거. 이 스크립트가 만든 것(marker 있음)만 지우므로
    #    손으로 쓴 _index.md 는 남는다.
    for existing in sorted(posts_dir.rglob("*.md")):
        route = existing.relative_to(posts_dir).as_posix()
        if route in written:
            continue
        if MARKER in existing.read_text(encoding="utf-8")[:2000]:
            if args.dry_run:
                print(f"[dry] remove {route}")
            else:
                existing.unlink()
                print(f"[rm]  {route}")

    # 5) 목차 노트가 없는 시리즈 폴더에는 최소 형태의 _index.md 를 만들어 둔다 (있으면 손대지 않음).
    for dir_slug, name in sorted(series_dirs.items()):
        index = posts_dir / dir_slug / "_index.md"
        if dir_slug in index_written or index.exists():
            continue
        if args.dry_run:
            print(f"[dry] new {index.relative_to(args.site)}")
        else:
            index.parent.mkdir(parents=True, exist_ok=True)
            index.write_text(series_index_stub(name), encoding="utf-8", newline="\n")
            print(f"[new] {index.relative_to(args.site)}")

    if not args.dry_run:  # 글이 모두 빠져나간 시리즈 폴더 정리
        for d in sorted((p for p in posts_dir.rglob("*") if p.is_dir()), reverse=True):
            if not any(d.iterdir()):
                d.rmdir()

    print(f"\n{len(written)}개 글 동기화 완료.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
