# j-skills workspace

3 skill: j-plan (planning), j-work (work log), yijing-fengshui (易经). GitHub: JacobYeh/j-skills.

## 3 skills
- j-plan/ - 计划/历史 (planning.md 是 source of truth)
- j-work/ - 工作日志
- yijing-fengshui/ - 易经数据 (jacob_bazi.md, jacob_birth.json)

## notify.py (每个 skill 都有)
走 push-hub (独立 repo: JacobYeh/push-hub, 本地 ~/projects/push-hub), dedup 60s, 4 优先级.
3 个 skill 共享 `_shared/notify_base.py`, 每个 skill 的 notify.py 是 10 行 wrapper (只声明 SOURCE).

## 用法
- jp "msg" - j-plan 通知
- jw "msg" - j-work 通知
- yj "msg" - 易经通知
- 各自都有 -dry 版本

## 关键文档
- j-plan/planning.md - 计划/历史
- j-plan/activity-log.md - 活动日志
- yijing-fengshui/data/jacob_bazi.md - 八字
