# -*- coding: utf-8 -*-
"""curly_quotes() 회귀 테스트. `python scripts/test_curly_quotes.py` 로 실행."""
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sync_from_vault import curly_quotes, protect_math  # noqa: E402

OPEN, CLOSE = "“", "”"

CASES = [
    # (이름, 입력, 기대 출력)
    (
        "조사가 붙은 인용 - 원래 깨지던 케이스",
        '가산은 "극한은 다룰 수 있으면서"는 지점이야.',
        f'가산은 {OPEN}극한은 다룰 수 있으면서{CLOSE}는 지점이야.',
    ),
    (
        "한 줄에 여러 쌍",
        '"길이", "넓이", "부피"라고 부른다.',
        f'{OPEN}길이{CLOSE}, {OPEN}넓이{CLOSE}, {OPEN}부피{CLOSE}라고 부른다.',
    ),
    (
        "이미 곱슬 따옴표면 그대로 (멱등)",
        f'{OPEN}그대로{CLOSE}다.',
        f'{OPEN}그대로{CLOSE}다.',
    ),
    (
        "코드스팬 안의 따옴표는 건드리지 않는다",
        'print("hello") 는 `print("hi")` 라고 쓴다.',
        f'print({OPEN}hello{CLOSE}) 는 `print("hi")` 라고 쓴다.',
    ),
    (
        "코드펜스 안의 따옴표는 건드리지 않는다",
        '앞 "말"\n```python\nx = "not touched"\ny = "also not"\n```\n뒤 "말"',
        f'앞 {OPEN}말{CLOSE}\n```python\nx = "not touched"\ny = "also not"\n```\n뒤 {OPEN}말{CLOSE}',
    ),
    (
        "짝이 안 맞는 줄은 건너뛴다",
        '이건 "짝이 없다',
        '이건 "짝이 없다',
    ),
    (
        "따옴표가 줄을 넘어가면 건드리지 않는다",
        '앞줄 "열고\n뒷줄 닫는다"',
        '앞줄 "열고\n뒷줄 닫는다"',
    ),
]


def main() -> int:
    failed = 0
    for name, src, want in CASES:
        got = curly_quotes(src)
        ok = got == want
        failed += 0 if ok else 1
        print(("PASS  " if ok else "FAIL  ") + name)
        if not ok:
            print("      want: " + repr(want))
            print("      got : " + repr(got))

    # protect_math 와의 통합: 따옴표 안에 수식이 들어 있는 실제 케이스
    src = '5강에서 $L^2$는 "$E[X^2]<\\infty$인 확률변수들의 모임"이었다.'
    got = curly_quotes(protect_math(src))
    ok = (
        got.count(OPEN) == 1
        and got.count(CLOSE) == 1
        and '"' not in got
        and "E[X^2]<\\infty" in got  # 수식 내용이 살아 있어야 한다
    )
    failed += 0 if ok else 1
    print(("PASS  " if ok else "FAIL  ") + "따옴표 안의 수식이 보존된다")
    if not ok:
        print("      got : " + repr(got))

    # 수식 블록 안의 따옴표는 보호된다
    src = '앞 "말"\n$$\n\\text{a "b" c}\n$$\n'
    got = curly_quotes(protect_math(src))
    ok = '\\text{a "b" c}' in got and got.count(OPEN) == 1
    failed += 0 if ok else 1
    print(("PASS  " if ok else "FAIL  ") + "블록 수식 안의 따옴표는 보호된다")
    if not ok:
        print("      got : " + repr(got))

    print("")
    print("failed: %d" % failed)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
