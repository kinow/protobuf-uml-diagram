#!/usr/bin/env python3

import tomllib
from pathlib import Path

CHAR_WIDTH = 7
PADDING = 10
MIN_LEFT_WIDTH = 45


def make_badge(label: str, value: str, color: str) -> str:
    left_width = max(MIN_LEFT_WIDTH, len(label) * CHAR_WIDTH + PADDING)
    right_width = len(value) * CHAR_WIDTH + PADDING
    width = left_width + right_width

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20" role="img" aria-label="{label}: {value}">
  <title>{label}: {value}</title>
  <linearGradient id="a" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <rect width="{width}" height="20" rx="3" fill="#555"/>
  <rect x="{left_width}" width="{right_width}" height="20" rx="3" fill="{color}"/>
  <rect width="{width}" height="20" rx="3" fill="url(#a)"/>
  <g fill="#fff" font-family="Verdana,Arial,sans-serif" font-size="11">
    <text x="{left_width / 2:.0f}" y="14" text-anchor="middle">{label}</text>
  </g>
  <g fill="#000" font-family="Verdana,Arial,sans-serif" font-size="11">
    <text x="{left_width + right_width / 2:.0f}" y="14" text-anchor="middle">{value}</text>
  </g>
</svg>
"""


def write_badge(name: str, label: str, value: str, color: str) -> None:
    output = Path(".github/badges") / f"{name}.svg"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(make_badge(label, value, color), encoding="utf-8")
    print(f"Wrote {output}")


def main() -> None:
    with Path("pyproject.toml").open("rb") as f:
        project = tomllib.load(f)["project"]

    version = project["version"]
    python_version = project["requires-python"].replace(">=", "")

    license_file = project["license"]["file"]
    license_name = Path(license_file).read_text(encoding="utf-8").splitlines()[0]

    write_badge(
        "pypi",
        "PyPI",
        f"v{version}",
        "#ffd343",
    )

    write_badge(
        "python",
        "Python",
        f">={python_version}",
        "#3776ab",
    )

    write_badge(
        "license",
        "License",
        license_name,
        "#999999",
    )


if __name__ == "__main__":
    main()
