param(
    [int]$PlayerCount = 12,
    [string]$PublicDir = "public",
    [string]$PrivateDir = "private",
    [string]$FirstRound = "Round01"
)

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$skillScript = Join-Path $repoRoot ".agents\\skills\\werewolf-game-reset\\scripts\\reset_game.ps1"

if (-not (Test-Path $skillScript)) {
    throw "Missing reset skill script: $skillScript"
}

& $skillScript `
    -PlayerCount $PlayerCount `
    -PublicDir $PublicDir `
    -PrivateDir $PrivateDir `
    -FirstRound $FirstRound `
    -RepoRoot $repoRoot
