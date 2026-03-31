from __future__ import annotations

import argparse
import json
import random
import secrets
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
POOL_PATH = ROOT / "references" / "personality_pool.json"

FIELD_ORDER = [
    ("summary", "一句话定位"),
    ("temperament", "核心气质"),
    ("day_speech", "白天发言习惯"),
    ("logic_focus", "逻辑抓手"),
    ("pressure_response", "被质疑时的反应"),
    ("role_expression", "不同身份下的表现"),
    ("voting_style", "投票与站边"),
    ("risk_profile", "风险偏好"),
    ("caution", "注意事项"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Randomly assign unique werewolf subagent personalities."
    )
    parser.add_argument(
        "--count",
        type=int,
        help="Number of unique personalities to draw. Defaults to 11 unless --seats is provided.",
    )
    parser.add_argument(
        "--seats",
        help="Comma-separated seat labels, for example P2,P3,P4.",
    )
    parser.add_argument(
        "--seed",
        help="Optional seed for reproducible draws. Omit to generate a fresh seed.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format. Defaults to markdown.",
    )
    return parser.parse_args()


def load_pool() -> list[dict[str, str]]:
    with POOL_PATH.open("r", encoding="utf-8") as handle:
        pool = json.load(handle)

    if not isinstance(pool, list):
        raise ValueError("personality pool must be a list")

    if len(pool) < 24:
        raise ValueError("personality pool must contain at least 24 personalities")

    ids = set()
    names = set()
    required_fields = {key for key, _ in FIELD_ORDER} | {"id", "name"}

    for entry in pool:
        if not isinstance(entry, dict):
            raise ValueError("each personality entry must be an object")
        missing = required_fields - entry.keys()
        if missing:
            raise ValueError(
                f"personality '{entry.get('name', '<unknown>')}' is missing fields: {sorted(missing)}"
            )
        if entry["id"] in ids:
            raise ValueError(f"duplicate personality id: {entry['id']}")
        if entry["name"] in names:
            raise ValueError(f"duplicate personality name: {entry['name']}")
        ids.add(entry["id"])
        names.add(entry["name"])

    return pool


def parse_seats(raw_seats: str | None) -> list[str]:
    if not raw_seats:
        return []

    seats = [seat.strip() for seat in raw_seats.split(",") if seat.strip()]
    if not seats:
        raise ValueError("at least one non-empty seat label is required when --seats is used")
    if len(set(seats)) != len(seats):
        raise ValueError("seat labels must be unique")
    return seats


def resolve_request(count: int | None, seats: list[str]) -> tuple[int, list[str]]:
    if seats:
        if count is None:
            count = len(seats)
        elif count != len(seats):
            raise ValueError("--count must match the number of seats when both are provided")
    elif count is None:
        count = 11

    if count <= 0:
        raise ValueError("--count must be greater than 0")

    if not seats:
        width = max(2, len(str(count)))
        seats = [f"Seat{index:0{width}d}" for index in range(1, count + 1)]

    return count, seats


def build_agent_brief(seat: str, persona: dict[str, str]) -> str:
    return (
        f"你负责 {seat}，固定性格为“{persona['name']}”。"
        f"{persona['temperament']} 白天请保持这样的说话气场：{persona['day_speech']} "
        f"盘逻辑时优先抓：{persona['logic_focus']} "
        f"受压时请按这个风格回应：{persona['pressure_response']} "
        f"不同身份都沿用这套人格外壳：{persona['role_expression']} "
        f"投票与站边请符合：{persona['voting_style']} "
        f"整体风险偏好是：{persona['risk_profile']} "
        f"额外注意：{persona['caution']}"
    )


def draw_personalities(
    pool: list[dict[str, str]], count: int, seed: str
) -> list[dict[str, str]]:
    if count > len(pool):
        raise ValueError(
            f"requested {count} personalities but pool only contains {len(pool)} entries"
        )
    rng = random.Random(seed)
    return rng.sample(pool, count)


def render_markdown(
    seats: list[str], selected: list[dict[str, str]], seed: str, pool_size: int
) -> str:
    lines = [
        "# 子代理性格抽取结果",
        "",
        f"- seed: `{seed}`",
        f"- 抽取人数: {len(selected)}",
        f"- 性格池大小: {pool_size}",
        f"- 重复策略: 同一批次无重复抽样",
        "",
        "## 使用提醒",
        "",
        "- 只把对应席位的区块发给对应子代理。",
        "- 不要把整张性格映射写入公开玩家文件。",
        "- 性格影响表达方式，但不覆盖规则和信息边界。",
        "",
    ]

    for seat, persona in zip(seats, selected):
        lines.append(f"## {seat} | {persona['name']}")
        lines.append("")
        for key, label in FIELD_ORDER:
            lines.append(f"- {label}: {persona[key]}")
        lines.append(f"- 发给子代理的摘要: {build_agent_brief(seat, persona)}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_json(
    seats: list[str], selected: list[dict[str, str]], seed: str, pool_size: int
) -> str:
    assignments = []
    for seat, persona in zip(seats, selected):
        enriched = dict(persona)
        enriched["seat"] = seat
        enriched["agent_brief"] = build_agent_brief(seat, persona)
        assignments.append(enriched)

    payload = {
        "seed": seed,
        "pool_size": pool_size,
        "draw_count": len(assignments),
        "unique_sampling": True,
        "assignments": assignments,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    try:
        args = parse_args()
        seats = parse_seats(args.seats)
        count, seats = resolve_request(args.count, seats)
        pool = load_pool()
        seed = args.seed or secrets.token_hex(8)
        selected = draw_personalities(pool, count, seed)

        if args.format == "json":
            output = render_json(seats, selected, seed, len(pool))
        else:
            output = render_markdown(seats, selected, seed, len(pool))

        sys.stdout.write(output)
        return 0
    except Exception as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
