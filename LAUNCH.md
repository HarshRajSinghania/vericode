# LAUNCH · VeriCode (Phase 8)

> Written to read like a human wrote it, not marketing copy. **All publish/posting
> actions are gated (⛔) — nothing below has been executed.**

## The honest pitch
I built VeriCode because I kept pasting AI-generated code into repos and only
*hoping* it worked. `vericode .` runs the checks that should've been obvious —
type-check, tests, secret scan, dependency CVEs — in one local command, no
account, no config. It caught a hardcoded Stripe key and 10 CVEs in a throwaway
sample on the first run. It's small, it's MIT, and the scanner is dependency-free.

---

## Show HN
**Title:** Show HN: VeriCode – verify AI-generated code actually works, in one local command

**First post:**
> I've been using coding agents a lot this year, and my recurring mistake is
> trusting code that *looks* right. So I built a tiny CLI that runs the "should've
> been obvious" checks before I commit: type-check, tests, hardcoded-secret scan,
> and a dependency CVE lookup.
>
> It's local-first and keyless — the CVE check hits the free OSV API anonymously,
> nothing leaves your machine otherwise. `vericode .` prints a table;
> `vericode . --strict` is the CI gate (non-zero exit on any problem).
>
> What I'm unsure about: is "one command for all of it" actually useful, or do
> people already have this wired up with separate tools? And the type-check/test
> steps intentionally *skip* (not pass) when the toolchain isn't installed, so it
> never lies about being green. Curious if that's the right call.
>
> MIT, Python. Would love feedback on what's missing.

---

## Reddit (2 subreddits, community-flavored)

### r/selfhosted — *not* a fit, skip. Use:
### r/programming
> Title: I made a CLI that runs the "should've been obvious" checks on AI-generated code before you commit
> Body: short version of the Show HN post, emphasis on local-first / no account,
> and the "skip ≠ pass" design decision. Ask: how do you currently gate AI code
> in your pipeline?
> *Self-promo rule check:* r/programming allows Show HN-style self posts if they're
> substantive and not spammy; keep it to one post, engage in comments, no repeated
> cross-posting.

### r/opensource
> Title: VeriCode: a local-first, MIT-licensed "verify AI code" CLI — looking for contributors
> Body: focus on the maintainer angle — small codebase, 77% tested, clear
> good-first-issues list. Ask what the first ecosystem to add should be.
> *Self-promo rule check:* r/opensource permits "look at my project" posts; keep
> it once, link repo + license, respond to every comment.

---

## X / Twitter — 5-tweet thread
1/ I pasted AI-generated code into a repo and it *looked* fine. It had a hardcoded
Stripe key and pulled a dependency with 10 CVEs. Built a tiny CLI so I'd stop
doing that: `vericode .`

2/ One command: type-check, run tests, scan for secrets, check dependency CVEs.
No account, no config, nothing leaves your machine (CVE lookup is keyless + anonymous).

3/ `vericode . --strict` is the CI gate — non-zero exit on any problem. Drop it
into GitHub Actions in 3 lines.

4/ Design choice I'm stubborn about: if the toolchain (mypy, tsc, go…) isn't
installed, it reports *skip*, never *pass*. A green check you didn't earn is worse
than no check.

5/ MIT, Python, ~400 lines of real logic + tests. Feedback welcome — especially
what's missing. (link)

---

## Product Hunt tagline
> VeriCode — Verify AI-generated code actually works: type-check, test, secret-scan
> and CVE-check in one local command. No account, no config.

---

## 中文版

### 掘金
标题：我用 AI 写代码踩的坑：它看起来对，其实藏着密钥和 10 个 CVE
正文：同 Show HN 故事线，强调"本地优先、零配置、免密钥查 CVE"，附
`vericode .` 输出截图（用 `--exclude tests` 的干净版）。结尾抛问题：你现在的
AI 代码准入流程是什么？

### V2EX
标题：[开源] VeriCode —— 一条命令验证 AI 生成的代码到底能不能用
正文：短，突出"skip 不等于 pass"的设计取舍，问大家第一个该加什么语言/生态。
遵守 V2EX 自荐版规：一次、附 GitHub 链接、回帖。

### 即刻
一条动态：用 3 句话讲清痛点 + 一条命令 + 链接，带 #独立开发 #AI编程 话题。

---

## 发布时间建议（按社区活跃时段，UTC+8）
- **Show HN / Hacker News:** 周二–周四 22:30–24:00（美西早间，HN 流量高峰）
- **r/programming, r/opensource:** 周三/周四 21:00–23:00
- **X / Twitter:** 上述时段同步发 thread，隔 30–45 分钟逐条发
- **掘金 / V2EX / 即刻:** 周四–周六 20:00–22:00（国内开发者活跃）
- 错峰，不一次性全平台铺开，便于逐个社区认真回帖。

## 发布后 72 小时响应清单
- [ ] 每个帖子/Issue/PR 认真回复，尤其是质疑（"已有 gitleaks/Snyk" → 说明差异表）
- [ ] 收集反馈进 `docs/initial-issues.md` 或新 Issue
- [ ] 快速修 bug（CI 红了立刻修，保持 main 常绿）
- [ ] 每天更新 CHANGELOG 与一条进度 tweet
- [ ] 对"skip ≠ pass"和"为何不用 X"两个问题准备标准答案，避免重复解释
- [ ] 72h 后汇总 Star 增长、流量来源、高频反馈 → 写入 RETRO.md（阶段 9）

---

## ⛔ 待你确认的动作（Orchestrator 不会自行执行）
1. `gh repo create LucasXlab/vericode --public` 并在组织 LucasXlab 下建库
2. 提交作者邮箱用 GitHub noreply 邮箱，推送到远程
3. 按 `docs/repo-settings.md` 设置 description / topics / labels
4. 批量开 `docs/initial-issues.md` 里的 6 个初始 Issue
5. 按本文件发布 Show HN / Reddit / X / 中文帖
确认后我才执行上述公开动作。
