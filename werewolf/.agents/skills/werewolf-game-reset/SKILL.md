---
name: werewolf-game-reset
description: Reset and scaffold the active werewolf game workspace for a fresh match by recreating `public/summary.md`, `public/rounds/Round01.md`, `private/main-agent/main-agent.md`, and `private/players/P1.md` through `P12.md`. Use when Codex is starting a new game, restarting after a completed match, clearing stale round logs, or rebuilding the default public/private file structure before spawning record subagents, assigning roles, and spawning player subagents.
---

# Werewolf Game Reset

Use this skill before the moderator starts a new match. It rebuilds the active `public/` files, the moderator's private night log, and the per-player private notebooks into the expected default layout for Round01.

## Quick Start

1. From the repository root, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\.agents\skills\werewolf-game-reset\scripts\reset_game.ps1
```

2. If the match setup differs, override parameters explicitly:

```powershell
powershell -ExecutionPolicy Bypass -File .\.agents\skills\werewolf-game-reset\scripts\reset_game.ps1 -PlayerCount 12 -FirstRound Round01
```

3. After reset completes, verify these active files exist:
- `public/summary.md`
- `public/rounds/Round01.md`
- `private/main-agent/main-agent.md`
- `private/players/P1.md` through `private/players/P12.md`
4. Confirm that `P2` through `P12` also contain placeholders for `### 本局性格档案` and `### 子代理恢复摘要` before you draw personalities.

## Workflow

1. Run the reset script before dealing roles, generating personalities, or asking players for private thoughts.
2. Treat the script as destructive for the active match workspace: it replaces the current round logs and active per-player private notebooks.
3. Preserve old transcripts elsewhere first if you need historical archives before starting a new match.
4. After reset, spawn the moderator support agents `public-writer` and `private-writer` so subsequent `public/` and `private/` writes can be delegated.
5. Then call the personality generator, privately assign roles, and fill each seat's `固定信息`; `P2` through `P12` must also receive their full persona archive and recovery summary before the first spawn.
6. Keep the full role mapping and other moderator secrets out of shared files even after reset; use `private/main-agent/main-agent.md` for minimal per-round night logs rather than dumping every secret.

## Resources

- Use `scripts/reset_game.ps1` for all normal resets. It recreates `public/summary.md`, `public/rounds/Round01.md`, `private/main-agent/main-agent.md`, and the 12 private player notebooks with the expected headings.
- The reset template keeps `P1` lightweight as the user seat, while `P2` through `P12` include persona archive and recovery-summary placeholders under `## 固定信息`.
