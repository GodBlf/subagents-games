param(
    [int]$PlayerCount = 12,
    [string]$PublicDir = "public",
    [string]$PrivateDir = "private",
    [string]$FirstRound = "Round01",
    [string]$RepoRoot = $(Resolve-Path (Join-Path $PSScriptRoot "..\\..\\..\\..")).Path
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$resolvedRepoRoot = (Resolve-Path $RepoRoot).Path
$publicRoot = Join-Path $resolvedRepoRoot $PublicDir
$roundsDir = Join-Path $publicRoot "rounds"
$privateRoot = Join-Path $resolvedRepoRoot $PrivateDir
$mainAgentDir = Join-Path $privateRoot "main-agent"
$playersDir = Join-Path $privateRoot "players"

New-Item -ItemType Directory -Path $publicRoot -Force | Out-Null
New-Item -ItemType Directory -Path $roundsDir -Force | Out-Null
New-Item -ItemType Directory -Path $privateRoot -Force | Out-Null
New-Item -ItemType Directory -Path $mainAgentDir -Force | Out-Null
New-Item -ItemType Directory -Path $playersDir -Force | Out-Null

# Replace only the active game logs and active private notebooks.
Get-ChildItem -Path $roundsDir -Filter "*.md" -ErrorAction SilentlyContinue | Remove-Item -Force
Get-ChildItem -Path $mainAgentDir -File -Filter "main-agent.md" -ErrorAction SilentlyContinue | Remove-Item -Force
Get-ChildItem -Path $playersDir -Filter "P*.md" -ErrorAction SilentlyContinue | Remove-Item -Force
Get-ChildItem -Path $publicRoot -File -Filter "summary.md" -ErrorAction SilentlyContinue | Remove-Item -Force
Get-ChildItem -Path $publicRoot -File -Filter "Round*.md" -ErrorAction SilentlyContinue | Remove-Item -Force
Get-ChildItem -Path $privateRoot -File -Filter "P*.md" -ErrorAction SilentlyContinue | Remove-Item -Force

$summaryContent = @"
# summary

## 本局概况
- 状态: 准备中
- 当前回合: $FirstRound

## 全局公开时间线
"@

Set-Content -Path (Join-Path $publicRoot "summary.md") -Value $summaryContent -Encoding UTF8

$roundContent = @"
# $FirstRound

## 回合概况
- 状态: 待主持填写

## 夜间公告

## 白天发言

## 投票与结算
"@

Set-Content -Path (Join-Path $roundsDir "$FirstRound.md") -Value $roundContent -Encoding UTF8

$mainAgentContent = @"
# main-agent

## 文档说明
- 用途: 记录主持在每回合夜间收到的行动、仲裁结果与次日对外口径
- 保密级别: 仅主持与 private-writer 可读写
- 记录原则: 只写最小必要私密信息，不在此强制维护全量身份映射

## 私密时间线

### $FirstRound
#### 夜间行动与结果

#### 仲裁备注

#### 对外口径
"@

Set-Content -Path (Join-Path $mainAgentDir "main-agent.md") -Value $mainAgentContent -Encoding UTF8

for ($i = 1; $i -le $PlayerCount; $i++) {
    $seat = "P{0}" -f $i
    $playerType = if ($i -eq 1) { "用户玩家" } else { "子代理玩家" }

    if ($i -eq 1) {
        $playerContent = @"
# $seat $playerType

## 固定信息
- 席位: $seat
- 玩家类型: $playerType
- 本局身份: 待主持私下填写
- 本局性格: 用户自行决定
- 当前状态: 存活

## 私密思考记录

### $FirstRound
#### 已知信息

#### 真实判断

#### 行动计划
"@
    }
    else {
        $playerContent = @"
# $seat $playerType

## 固定信息
- 席位: $seat
- 玩家类型: $playerType
- 本局身份: 待主持私下填写
- 本局性格: 待主持私下填写
- 当前状态: 存活

### 本局性格档案
- 性格ID: 待主持私下填写
- 一句话定位: 待主持私下填写
- 核心气质: 待主持私下填写
- 白天发言习惯: 待主持私下填写
- 逻辑抓手: 待主持私下填写
- 被质疑时的反应: 待主持私下填写
- 不同身份下的表现: 待主持私下填写
- 投票与站边: 待主持私下填写
- 风险偏好: 待主持私下填写
- 注意事项: 待主持私下填写

### 子代理恢复摘要
待主持私下填写

## 私密思考记录

### $FirstRound
#### 已知信息

#### 真实判断

#### 行动计划
"@
    }

    Set-Content -Path (Join-Path $playersDir "$seat.md") -Value $playerContent -Encoding UTF8
}
