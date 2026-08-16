---
name: j-plan
description: Jacob's personal planning and reminder system. Manages yearly, monthly, and weekly plans with history tracking, AI-powered summary, and Feishu weekly report delivery. Use when Jacob asks about plans, reminders, planning history, or weekly review.
---

# J-Plan — Personal Planning & Reminder System

## Push 模板变量 (host 替换)

cron prompt 推送时使用的占位符, 由 host 在调 push-hub 前替换:
- `{{FEISHU_USER_OPEN_ID}}` — Jacob 个人飞书 open_id (从 push-hub chat config 取)
- `{{FEISHU_CHAT_ID}}` — 群 chat_id (群推送时用)

**不要**直接复制 `{{...}}` 到 push 调用, 必须 host 层替换.

## Overview

Jacob's planning assistant that tracks yearly, monthly, and weekly plans with full history. Provides AI summaries, queries past records, and delivers weekly reports via Feishu.

## File Locations

| File | Description |
|------|-------------|
| `planning.md` | **唯一真实数据源** — 年度/月度/周计划、原则、7 月工作日纪律、AI 主线 |
| `planning_raw.txt` | ⚠️ _历史说明:_ 原始 full-text（2019-2026 未压缩, 96K）已并入 `planning.md`。本技能当前不维护独立 raw 文件 — 避免双数据源不一致 |
| `history-index.md` | 自动生成的索引（关键转折点 + 周/月状态） |
| `activity-log.md` | 活动日志 |

## Querying Full History

Jacob can query by asking:
- "Show me the week of [date]"
- "What did I plan for [month/year]"
- "Find all entries about [topic]"

The assistant reads `planning.md` (唯一真实数据源) and searches for matching content. 2019-2026 历史数据已并入文件。

## Planning File Format

**Active file:** `planning.md` — 唯一读写数据源。年/月/周用 `##` 标题分块，每周自带"目标 / 跨期 / 已回填 / 自查 / 复盘"5 个标准小节。

> 💡 旧版"raw 文件 + 摘要"的双源结构已废弃。
> 合并到 planning.md 后, 写入冲突 / 同步漂移的问题消失, AI 不用先读 raw 再读 planning.

## Core Functions

### 1. Read & Update Planning File

**Reading:** Use `exec` with `cat` or `type` on Windows, or read from synced location.

**Writing:** Write new entries in markdown format, append to the appropriate section.

### 2. History Query

Jacob can ask:
- "Show me my plans from last month"
- "What did I plan for Q2?"
- "History of work goals"
- "Show all weekly reviews from January"

The skill maintains a structured index of entries by date and category.

### 3. AI Summary & Analysis

When Jacob queries history, the skill:
- Searches relevant date ranges
- Identifies patterns (completed vs dropped items)
- Gives a concise summary with stats
- Compares periods if requested

### 4. Weekly Micro-Review via Feishu (Sunday 8 PM)

> 🎯 _设计原则:_ **简单 / 人性 / 高效**
> - **简单** — 5 个字段代替报告
> - **人性** — 像朋友对话，不是结构化表单
> - **高效** — Jacob 30 秒填完，AI 30 秒归档，零追问
>
> _重写于 2026-07-05 — Jacob 反馈"原周报像年终总结, 没人想读"_

A weekly cron job (`J-Plan-Weekly-Review`) runs every **Sunday 8:00 PM (Asia/Shanghai)** and operates in two micro-steps.

#### Step 1 — AI 推送（开篇问候 + 5 字段收件箱）

> 💬 推送内容模板（发送至 Jacob via Feishu DM, `user:{{FEISHU_USER_OPEN_ID}} — 从 push-hub chat config 自动取`）：
> 
> ```
> 周日 8 点了, 走个 30 秒版
> 
> 回 5 行就行:
> 1) a-g 工作交付: 几项完成 / 7?     (e.g. "5/7")
> 2) 5 个动作纪律: 平均几分?          (e.g. "3.5")
> 3) 运动: X 次? (hypergym ___ / 游泳 ___ / supermonkey ___)
> 4) 这周最值的一件事: 一句话
> 5) 下周最想做的一件事: 一句话
> 
> 崩的地方直接喊就行, 不用写完整句.
> 
> 实在懒得回?
> - "还行"   → 我从数据里帮你归档
> - "下次再说" → 我跳过本周
> ```

**设计点：**
- **不预生成报告** — Jacob 回什么才是真的，没回就没有
- **5 字段覆盖度足够**：a-g (工作) + 纪律 (P0) + 运动 (体) + 复盘 (心) + 下周 (前瞻)
- **留两个逃逸口** — "还行 / 下次再说"，避免周复盘变成负担

#### Step 2 — Jacob 回完 → AI 归档

收到 Jacob 回复后，AI 只做三件事，按顺序：

1. **把 5 字段写入** `planning.md` 的对应周（已回填、自查、复盘、跨期）
2. **更新** `history-index.md`（写一行该周摘要）
3. **结束**：不发追问，不总结，不给"AI 建议"——除非 5 字段分 < 3（说明本周明显异常），否则零文字输出

**触发条件（轻量追加）：**
- 5 字段分 < 3 → 加一句（≤ 2 行）观察，写进规划文件
- 5 字段分 ≥ 3 → 静默归档，不打扰

#### 完整流程示例（最常见场景）

```
[Sun 20:00  AI → Jacob]
周日 8 点了, 走个 30 秒版

回 5 行就行:
1) a-g 工作交付: 几项完成 / 7?
2) 5 个动作纪律: 平均几分?
3) 运动: X 次?
4) 这周最值的一件事: 一句话
5) 下周最想做的一件事: 一句话

[Sun 20:14  Jacob → AI]
3.5/7
2.8
hyper 1, 游 3, super 0
实习收尾被老板夸了一下, 第一次觉得被看见
下周把 VDI 故障分类初版出了

[Sun 20:14+10s  AI 归档 → planning.md]
  a-g 完成度 3.5 / 7
  纪律均分 2.8
  运动: hyper 1 / 游 3 / super 0 (合计 4)
  ⭐ 实习收尾被夸 — 工作可见度提升
  下周重点: VDI 故障分类初版
  (纪律分 < 3, AI 追加一行:)
  → 纪律 2.8 偏弱, 中午漱口冥想和 9 点写计划是跌点; 下周一 09:00 加 1 行补救.

[Silent end — 不发追问]
```

**对比旧版（改前）：** 6 段大报告 + Jacob 写 4 段回复 + AI 写回全表 + AI 再补 2-3 条建议
**对比新版（改后）：** 1 条问候 + 5 行数字 + AI 1 段归档 + 静默结束
**节省：** Jacob 侧 5 分钟 → 30 秒；AI 侧 4 段输出 → 1 段归档

---

## Planning File Format (Recommended)

If the .one file is not accessible, maintain a synced markdown version:

```markdown
# 📅 年度计划 [YEAR]

## 🎯 年度目标
- [ ] Goal 1
- [x] Goal 2

---

# 📆 月度计划 [YEAR-MONTH]

## 🎯 本月重点
- [ ] Task
- [x] Task

## ✅ 完成情况
- Completed item

## 📝 备注
- Notes

---

# 📊 周计划 [YEAR-WEEK]

## 📅 [Start Date] - [End Date]

## 🎯 本周目标
- [ ] Task 1
- [ ] Task 2

## 🔄 跨期任务
- [ ] Task from last week

## ✅ 完成记录
- [x] Done

## 📝 复盘
- What went well
- What to improve

---

# 📜 历史记录索引

| Date | Type | Summary | Status |
|------|------|---------|--------|
| 2026-04-28 | Weekly | Focus on XXX | Completed |
| 2026-05-05 | Weekly | Work on YYY | Partial |
| 2026-05-12 | Weekly | ZZZ | Completed |
```

---

## Cron Jobs (Auto-Schedule)

| Job | Schedule | Purpose |
|-----|----------|---------|
| **J-Plan-Weekly** | Every Monday 9:00 AM | Preview next week + ask for updates |
| **J-Plan-Weekly-Review** | Every Sunday 8:00 PM | Review past week + seek feedback + plan下周 |
| **J-Plan-Monthly-Review** | Last day of month 8:00 PM | Review past month + next month proposal |
| **J-Plan-Yearly-Review** | Dec 31 8:00 PM | Year review + next year proposal |

All four jobs send directly to Jacob via Feishu DM and wait for his reply before writing back to planning files.

---

## Weekly Cron Job — J-Plan-Weekly

**Schedule:** Every Monday 9:00 AM (Asia/Shanghai)
**Session:** Isolated
**Timeout:** 120 seconds

**用途：** 周一 9 点 — 用 4 个问题帮 Jacob 锁定本周

**Prompt:**
```
你是一个周计划助理 J-Plan.

1. 读 planning.md 最新一周的"🎯 本周目标"区（skill 目录下的 `planning.md`）
2. 通过 Feishu DM 给 Jacob 发一条简短问候 + 4 字段微前瞻:
   - 本周最重要的 1 件事 (from planning.md, 一句话)
   - 5 个动作纪律里本周最重点的 1 个
   - 运动节奏预期 (hypergym X / 游泳 Y / supermonkey Z)
   - 跨期任务前 3 个
3. 短结尾: "周一早上 9 点 09:00 你确认下要不要调"
4. 等回复. 收到后写回 planning.md 对应周的"跨期任务"区 (不重写其他部分).

Target: Jacob 个人 DM (user:{{FEISHU_USER_OPEN_ID}} — 从 push-hub chat config 自动取)
```

**改动点（vs 老版）：**
- 老版：4 段大报告 (上周完成/跨期/本周/AI 建议) + 等完整回复 + 写回全表
- 新版：4 字段微前瞻 + 一句话结尾 + 周一 9 点确认式对话
- 老版要读 planning_raw.txt（不存在）→ 新版只读 planning.md 一段

---

## Weekly Review Cron — J-Plan-Weekly-Review ⭐

**Schedule:** Every Sunday 8:00 PM (Asia/Shanghai) — `0 12 * * 0`
**Session:** Isolated
**Timeout:** 120 seconds

**用途：** 周日 8 点 — 5 字段微复盘（详见上面 "Step 4. Weekly Micro-Review"）

**Prompt:**
```
你是一个周日微复盘助理 J-Plan-Review.

1. 通过 Feishu DM 给 Jacob 发 5 字段微复盘收件箱（详见 Section 4 Step 1 模板）：
   - a-g 工作交付: 几项 / 7
   - 5 个动作纪律均分
   - 运动: hyper ___ / 游 ___ / super ___
   - 这周最值的一件事 (一句话)
   - 下周最想做的事 (一句话)
2. 留两个逃逸口: "还行" / "下次再说"
3. 等回复. 收到后:
   - 把 5 字段归档到 planning.md 对应周（已回填/自查/复盘/跨期区）
   - 更新 history-index.md
   - **如果 5 字段分 < 3，加一句 (≤ 2 行) 观察；否则静默结束**
   - **不追问**

Target: Jacob 个人 DM (user:{{FEISHU_USER_OPEN_ID}} — 从 push-hub chat config 自动取)
```

**改动点（vs 老版）：**
- 老版 prompt 引用不存在的 `planning_raw.txt` → 新版只引用 `planning.md`
- 老版要求生成完整 "weekly review + next week proposal" 报告 → 新版只发 5 字段收件箱
- 老版"等回复后写全表" → 新版"归档到对应区"
- 新版增加了"分 < 3 才轻追加"的退出条件

---

## Monthly Review Cron — J-Plan-Monthly-Review

**Schedule:** Last day of month 8:00 PM (Asia/Shanghai) — `0 12 28-31 * *`
**Session:** Isolated
**Timeout:** 300 seconds

**Prompt:**
```
You are J-Plan assistant. Your role:
1. Read planning.md (skill 目录下, 已合并 2019-2026 全部历史 — 旧 `planning_raw.txt` 已废弃)
2. Determine the current month and next month
3. Search planning.md for all weekly entries in the current month
4. Generate a monthly review + next month proposal:

Send the report directly to Jacob via Feishu DM.
Wait for Jacob's reply, then write the agreed monthly plan into planning.md (append as monthly entry) and update history-index.md.
```

---

## Yearly Review Cron — J-Plan-Yearly-Review

**Schedule:** December 31 8:00 PM (Asia/Shanghai) — `0 12 31 12 *`
**Session:** Isolated
**Timeout:** 300 seconds

**Prompt:**
```
You are J-Plan assistant. Your role:
1. Read planning.md (skill 目录下, 已合并 2019-2026 全部历史)
2. Determine the current year and calculate all monthly entries for it
3. Generate a full year review + next year proposal:

Send the report directly to Jacob via Feishu DM.
Wait for Jacob's reply, then write the agreed yearly plan into planning.md (append as new year entry) and update history-index.md.
```

---

## How to Use

### Query History
- "What did I plan for May?"
- "Show my Q2 goals"
- "Last week's review"

### Get Summary
- "Summarize my April"
- "How did March compare to February?"

### Update Plan
- "Add [task] to this week"
- "Move [task] to next week"
- "Mark [task] as done"

---

## Data Storage

- **Primary:** `planning.md` (skill 目录)
- **Index:** `history-index.md`
- **Logs:** `activity-log.md`

> 💡 路径都是相对 skill 目录, Mac/Linux/Windows 一致。旧 Windows 路径 `C:\Users\Jacob\.mavis\skills\j-plan/*` 已废弃 (Planning.one → planning.md 转换完成)。

---

Last updated: 2026-07-05 (Weekly Section 4 + Weekly/Weekly-Review cron prompts 重写为 5 字段微复盘)