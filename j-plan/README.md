# j-plan

## 共享 secrets path (跨 repo)

所有 j-skill + finance-advisor 共享同一份 secrets:

`~/.config/finance-advisor/secrets/secrets.env` (从 `~/projects/secrets/secrets.env.age` age-encrypted, bashrc 自动 decrypt)

包含: `FEISHU_APP_ID`, `FEISHU_APP_SECRET`, `FEISHU_CHAT_ID`, `FEISHU_USER_OPEN_ID` + 8 个其他 key.

⚠️ **不要**单独改路径 — finance-advisor 的 `workspace.py` + bashrc 都引用此路径. 改名/迁移时需同步 4 处:
1. `~/projects/secrets/secrets.env.age` (源)
2. `~/.bashrc` lines 128-134 (decrypt block)
3. `~/projects/finance-stack/skills/finance-advisor/scripts/workspace.py` (PROFILE_FILE 等)
4. push-hub `cli.py:74` + `channels/feishu_app.py:15` + `channels/feishu_webhook.py:16` (FEISHU secrets 读取)

## 通知 (push-hub)

跟 finance-advisor 一样, 本 skill 也接入了 push-hub 统一推送:

```bash
# 推文字
python3 notify.py --text "今天完成了 X" --priority normal

# 推 markdown 文件
python3 notify.py --file planning.md --title "周计划" --priority high

# Dry-run 模式
python3 notify.py --text "test" --dry-run
```

配置: 飞书 credentials 从 `~/.config/finance-advisor/secrets/secrets.env` 加载 (跟 finance-advisor 共享, 走 push-hub).
push-hub: 独立 repo [JacobYeh/push-hub](https://github.com/JacobYeh/push-hub) (本地 `~/projects/push-hub/`).
