---
name: werewolf-subagent-personality-generator
description: Generate randomized, non-repeating personalities for werewolf or mafia subagents in multi-agent social deduction games. Use when Codex needs to create or refresh agent seat personas, assign one distinct speaking style per seat, produce moderator-ready seat briefs, or keep a full table diverse across public reasoning, pressure style, vote posture, claim timing, and discussion rhythm.
---

# Werewolf Subagent Personality Generator

Use this skill to assign distinct seat personalities before the moderator spawns or briefs werewolf subagents.

## Quick Start

1. Draw personalities for the whole table in one batch so uniqueness is enforced in one run.
2. For this repository's 12-player game, run:

```powershell
python .\.agents\skills\werewolf-subagent-personality-generator\scripts\generate_personalities.py --count 11 --seats P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,P12
```

3. For each seat, copy only the matching seat block into that seat's `private/players/Pn.md`, filling `### 本局性格档案` and `### 子代理恢复摘要`.
4. After the private file is updated, use that same seat's `### 子代理恢复摘要` as the setup prompt for the first spawn.
5. Keep the draw private. Do not write the full mapping to public player history files.

## Workflow

1. Re-roll at the start of each new game unless you intentionally need a reproducible lineup.
2. Pass `--seed <value>` when you need deterministic replay for debugging, rematches, or transcripts.
3. Pass `--format json` when another tool needs structured output for writing `### 本局性格档案` and `### 子代理恢复摘要`.
4. Write each seat's full persona fields into only that seat's private notebook; do not rely on the initial spawn prompt as the only memory source.
5. Edit `references/personality_pool.json` only when you need to expand or rebalance the pool.
6. Stop and extend the pool before drawing if the requested seat count exceeds the pool size.

## Output Handling

- Treat each generated personality as a stable seat-level speaking style for the whole match.
- Persist each generated personality into that seat's `private/players/Pn.md` as the authoritative persona record for the match.
- Store both the structured persona fields and a restorable long-form summary so a replacement agent can recover without re-rolling.
- Let the personality affect wording, pacing, pressure style, claim posture, and vote behavior.
- Do not let the personality override rule compliance, role secrecy, or information boundaries.
- Give each subagent only its own generated block; do not leak the full table mapping to every agent.

## Respawn / Recovery

- If a seat's subagent crashes, respawn the same seat instead of drawing a new personality.
- On respawn, restore from that seat's `private/players/Pn.md`, especially `### 本局性格档案`, `### 子代理恢复摘要`, and `## 私密思考记录`.
- Do not treat the original spawn prompt as the only source of truth. The private notebook is the long-lived authority.
- Do not rewrite the persona on respawn unless the moderator explicitly starts a new game and re-rolls the full table.

## Resources

- Use `scripts/generate_personalities.py` for all normal draws. The script loads the pool, samples without replacement, supports optional seeds, and emits moderator-ready seat briefs.
- Read `references/personality_pool.json` only when editing or auditing the pool. The script already enforces uniqueness and formats the downstream prompt text.
