# j-skills

> Personal skills library — `j-plan` / `j-work` / `yijing-fengshui`.
> 与代码 repo `finance-stack` 分离, 这里是"我是谁", 那里是"怎么跑"。
> 2026-08-02 首次整理 + 推 GitHub。

## ✨ 是什么

`j-skills` 是 **个人技能包** 集合, 每个 skill 是独立的"能力描述 + 模板 + 数据"单元:

- `j-plan/` — 个人计划/年度复盘/习惯追踪
- `j-work/` — IT 工作指南 (Jump Trading 经验) + 面试准备
- `yijing-fengshui/` — 玄学辅助 (八字/起名/择日, 娱乐性质)

跟 `finance-stack` 的关系:
- `finance-stack` = 跑批/分析/推送的**代码** (Python 脚本)
- `j-skills` = **技能描述 + 个人数据** (SKILL.md + 模板 + 私人档案)
- Mavis agent 同时加载两边, 跨 skill 协作

## 📁 结构

```
j-skills/
├── README.md                       # 本文件
├── .gitignore                      # 排除 .DS_Store / 编辑器临时
├── j-plan/                         # 个人计划
│   ├── SKILL.md                    # Mavis skill 描述
│   ├── planning.md                 # 主计划 (年度/月度/周)
│   ├── planning-template.md        # 模板
│   ├── activity-log.md             # 活动日志
│   └── history-index.md            # 历史索引
├── j-work/                         # IT 工作
│   ├── SKILL.md
│   └── README.md                   # 完整职业指南 (15KB)
└── yijing-fengshui/                # 玄学
    ├── SKILL.md                    # (新写, 源没)
    ├── README.md                   # (新写, 源没)
    └── data/
        ├── jacob_birth.json        # 出生信息
        └── jacob_bazi.md           # 八字档案
```

## 🔒 隐私说明

| 文件 | 隐私级别 | 说明 |
|---|---|---|
| `j-plan/*.md` | 🟡 中 | 含个人目标/习惯/时间, 私人 |
| `j-work/README.md` | 🟡 中 | 含具体公司 (Jump Trading) + 同事 |
| `yijing-fengshui/data/*` | 🔴 高 | 出生信息 + 八字, 高度私人 |

**推送到 Private repo** — 加密访问 + GitHub 账号安全。
**不要**:
- ❌ 转 public repo
- ❌ 分享链接给不信任的人
- ❌ 在 .gitignore 漏数据时 push

## 🚀 跨 repo 协作

```bash
# Clone 两个 repo 到相邻目录
git clone https://github.com/JacobYeh/j-skills.git
git clone https://github.com/JacobYeh/finance-stack.git

# Mavis agent 加载 (自动)
# - 读 SKILL.md 注册 skill
# - 跨 skill 调用 (j-plan + finance-advisor 一起规划)
```

## 🛠️ 维护规则

1. **每次重大事件后更新** (换工作/年度复盘) — 推一次 commit
2. **私人数据先看隐私** — 推前想"这能不能让同事看到"
3. **跟 finance-stack 同步更新** — skill 描述变了, mavis 行为会变, 提前通知

## 📅 更新日志

- **2026-08-02** — 首次从散落位置整理, 推到 `JacobYeh/j-skills` private repo
  - j-plan: 从 `C:\Users\Jacob\.minimax\skills\j-plan\` 迁
  - j-work: 从 `C:\Users\Jacob\J-Mavis\skills\j-work\` 迁
  - yijing-fengshui: 从 workspace 迁, 补 SKILL.md + README.md

---

_4 个 skill 跟 code 解耦: 技能描述变, 不用动 Python 代码。_


## 通知 (push-hub)

每个 skill 都有自己的 `notify.py` 走 push-hub, 见各 skill 目录的 README.
push-hub 是独立 repo: [JacobYeh/push-hub](https://github.com/JacobYeh/push-hub) (本地 `~/projects/push-hub/`).
