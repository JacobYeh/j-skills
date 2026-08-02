# j-plan



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

配置: 飞书 app_id / app_secret / chat_id 在 `~/.openclaw/openclaw.json` (跟 finance-advisor 共享)。
