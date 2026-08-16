# Yijing-Fengshui (j-skills 子模块)

> 易经/八字/起名辅助 — 个人娱乐 + 自我反思, 不当决策依据。
> 2026-08-02 移到 j-skills repo。

## 数据

- `data/jacob_birth.json` — 出生信息 (公历 1987-03-06 丑时, 甘肃玉门)
- `data/jacob_bazi.md` — 四柱八字完整档案

## 设计原则

1. **娱乐优先** — 跟 j-plan/finance-advisor 比, 优先级最低
2. **数据本地** — 出生信息属隐私, 即使在 private repo 也要小心
3. **不做决策** — 投资/职业/婚姻 重大决策不靠八字
4. **可重写** — 推算逻辑出错时优先修正, 不维护错误结果

## 不建议做的事

- ❌ 用八字做投资标的筛选
- ❌ 用择日决定重要签约
- ❌ 用起名当小孩大名
- ❌ 把 AI 的命理解读当真

## 启用方式

```yaml
# mavis 系统的 skills 注册
name: yijing-fengshui
description: ...
```

---

_AI 时代的"赛博算命" — 留个念想, 别太当真。_


## 通知 (push-hub)

### 共享 secrets path (跨 repo)

所有 j-skill + finance-advisor 共享同一份 secrets:

`~/.config/finance-advisor/secrets/secrets.env` (从 `~/projects/secrets/secrets.env.age` age-encrypted, bashrc 自动 decrypt)

包含: `FEISHU_APP_ID`, `FEISHU_APP_SECRET`, `FEISHU_CHAT_ID`, `FEISHU_USER_OPEN_ID` + 8 个其他 key.

⚠️ **不要**单独改路径 — finance-advisor 的 `workspace.py` + bashrc 都引用此路径. 改名/迁移时需同步 4 处:
1. `~/projects/secrets/secrets.env.age` (源)
2. `~/.bashrc` lines 128-134 (decrypt block)
3. `~/projects/finance-stack/skills/finance-advisor/scripts/workspace.py` (PROFILE_FILE 等)
4. push-hub `cli.py:74` + `channels/feishu_app.py:15` + `channels/feishu_webhook.py:16`

### 用法

跟 finance-advisor 一样, 本 skill 也接入了 push-hub 统一推送:

```bash
# 推文字
python3 notify.py --text "今天完成了 X" --priority normal

# 推 markdown 文件
python3 notify.py --file planning.md --title "周计划" --priority high

# Dry-run 模式
python3 notify.py --text "test" --dry-run
```

配置: 飞书 3 个 key (`FEISHU_APP_ID` / `FEISHU_APP_SECRET` / `FEISHU_CHAT_ID`) 在 `~/.config/finance-advisor/secrets/secrets.env` (age-encrypted, bashrc 自动 decrypt).
push-hub: 独立 repo [JacobYeh/push-hub](https://github.com/JacobYeh/push-hub) (本地 `~/projects/push-hub/`).
