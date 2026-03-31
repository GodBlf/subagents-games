# 游戏架构说明

这份文档定义当前仓库中狼人杀多代理局的工作区结构、记录职责和子代理访问边界。目标是把“公开世界”和“私密思考”拆开，同时让主持能够稳定复盘每一轮。

## 目录结构

```text
public/
  summary.md
  rounds/
    Round01.md
    Round02.md
    ...
private/
  players/
    P1.md
    P2.md
    ...
    P12.md
scripts/
  Initialize-WerewolfGame.ps1
.agents/
  skills/
    werewolf-game-reset/
      scripts/
        reset_game.ps1
```

## 职责划分

- `public/summary.md` 是全局公开时间线，适合子代理快速补齐上下文。
- `public/rounds/RoundNN.md` 是某一轮的完整公开实录，保存该轮夜间公告、发言、投票和结算。
- `private/players/Pn.md` 是单席位的长期私密笔记，连续记录该席位每轮的真实想法和行动计划。

## 读写矩阵

- 主持：可读写全部 `public/**` 与 `private/**`。
- 子代理 `Pn`：可读 `public/**` 与 `private/players/Pn.md`；只可写 `private/players/Pn.md`。
- 子代理 `Pn`：禁止读取 `private/players/` 中其他席位文件；禁止写入任何 `public/**` 文件。

## 推荐回合写法

`private/players/Pn.md` 推荐按下面的结构持续追加：

```markdown
## 私密思考记录

### Round01
#### 已知信息
- 主持公开了什么
- 自己额外知道什么

#### 真实判断
- 当前最像狼的是谁，原因是什么
- 当前最像好人的是谁，原因是什么

#### 行动计划
- 夜间准备怎么行动
- 白天准备怎么发言
```

`public/rounds/RoundNN.md` 推荐按下面的结构维护：

```markdown
# Round01

## 回合概况
- 夜晚是否平安
- 白天发言顺序

## 夜间公告
- 主持公开宣布的死亡或平安夜信息

## 白天发言
- P1: ...
- P2: ...

## 投票与结算
- 放逐结果: ...
- 遗言: ...
```

## 主持工作流

1. 开局时调用 `werewolf-game-reset` skill，重建 `public/` 和 `private/players/`。
2. 私下发送身份与性格摘要给每个席位，并要求席位先写自己的私密文件，再给行动或发言。
3. 每次有公开事件发生时，只由主持更新 `public/summary.md` 与当前 `public/rounds/RoundNN.md`。
4. 每次子代理需要思考时，只给它两类可读路径：全部 `public/**` 和自己的 `private/players/Pn.md`。
5. 游戏结束后保留当前记录用于复盘；开启下一局前再重置。

推荐命令：

```powershell
powershell -ExecutionPolicy Bypass -File .\.agents\skills\werewolf-game-reset\scripts\reset_game.ps1
```

## 子代理提示词契约

主持给子代理下任务时，建议显式带上以下约束：

```text
你是 P5。
允许读取: public/summary.md, public/rounds/*.md, private/players/P5.md
允许写入: private/players/P5.md
禁止读取: private/players/ 中除 P5.md 外的其他文件
禁止写入: public/ 下任何文件

先把你本轮的真实想法追加到 private/players/P5.md。
然后只基于公开信息和你自己的私密信息返回行动或发言。
```

## 设计取舍

- 用 `summary.md` 做公开单点入口，避免子代理每次都全量读所有轮次。
- 用“一人一份私密文件”而不是“一轮一份私密文件”，避免主持在长局中维护大量零散文件。
- 公开文件只允许主持写，避免发言记录和仲裁结果出现多方并发覆盖。
- 私密文件允许席位自己维护，可以保留该席位稳定的长期推理链，而不是只保留最终公开发言。
