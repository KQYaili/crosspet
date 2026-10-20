# Linux 上的核对说明

这份说明给在 Linux 上工作的 Claude。只做下面列出的测试，以及测试失败时的小范围改代码。不要启动 CrossPet，不需要显示器，也不要把钩子装进自己的用户目录。

## 拉哪一份

账号 fork：<https://github.com/KQYaili/crosspet>

默认分支 `main` 仍是作者仓库的 1.3.6，没有这些修改。要拉分支 `grok-cursor-state-order`。

```bash
git clone https://github.com/KQYaili/crosspet.git
cd crosspet
git checkout grok-cursor-state-order
```

已经克隆过的话：

```bash
git fetch origin grok-cursor-state-order
git checkout grok-cursor-state-order
```

这个 fork 的远程名可能叫 `origin`。不要去拉 `lokicorvus/crosspet` 的 `main` 来覆盖这条分支。

## 分支里已经有的模块

- `integrations/crosspet-hook.py`：Codex 一轮结束后，迟到事件不能把角色拉回思考。子代理的事件（带 `agent_id`）不开始、不结束主线程的这一轮；手动 `/compact` 单独算一轮。Linux 上用 `fcntl` 加锁，可以直接测。
- `app/web/index.html`：切角色时作废上一名角色的延迟计时器；换角色那 0.33 秒里到的卡片、庆祝、重置提醒、彩蛋等换完再演。`ui_ownership_test.cjs` 抽函数测，`page_switch_test.cjs` 跑整段页面脚本，都不打开窗口。
- `integrations/cursor/crosspet-cursor-bridge.py`：Cursor 观察者钩子。Windows 用管道和 `msvcrt` 锁，macOS / Linux 用 `select` 和 `fcntl`。`cursor_bridge_test.py` 在临时目录里跑它；不要拿它写真实的状态目录。
- `tools/integrate.py`、`integrations/cursor/hooks.json`：接入 Cursor 的安装逻辑，两边都把桥接脚本放进运行目录。不要对真实的 `~/.cursor/hooks.json` 跑安装，测试里用临时目录。
- `characters/grok/`：Grok 的立绘和 `character.json`。
- `characters/claude/`：原有立绘，加上 `ip_detective.webp`、`suspend_lesson.webp`、`suspicious_pout.webp`。
- `app/windows/apps.json`：`cursor.exe` 对应 `grok`。

没有放进仓库的东西不要补：某台 Windows 电脑上为了绕过 Codex 目录虚拟化而写死的本机路径，提示词草稿，未选用的备用图。

## 要跑的测试

需要 `python3` 和 `node`。每条都要退出码 0。

```bash
python3 tests/character_assets_test.py
python3 tests/codex_turn_order_test.py
python3 tests/hook_stdin_test.py
python3 tests/hook_dataflow_test.py
python3 tests/cursor_bridge_test.py
python3 tests/integrate_test.py
node tests/ui_ownership_test.cjs
node tests/page_switch_test.cjs
```

这些测试只用临时目录和仓库里的文件。它们不会打开桌宠，也不会写当前用户的 CrossPet 数据目录。

## 可以改什么

测试失败，而且失败原因在下面这些文件里时，可以改代码，改完重跑同一组测试：

- `integrations/crosspet-hook.py`
- `app/web/index.html` 里的角色计时器
- `tests/` 里断言写错的地方
- `characters/*/character.json` 里指向不存在立绘的配置。缺图就改配置或在说明里记下，不要自己画，也不要删已有的 webp

## 不要做

- 不要运行 `install.sh`、`uninstall.sh`，不要执行 `tools/integrate.py install`
- 不要在测试以外跑 `integrations/cursor/crosspet-cursor-bridge.py`，也不要让它写真实的状态目录
- 不要动 Cursor 桥里 Windows 的那一半（管道和 `msvcrt` 锁）。macOS / Linux 走的是另一半
- 不要改其他角色的立绘像素
- 不要把本机绝对路径、用户名、密钥写进仓库
- 不要推送到 `lokicorvus/crosspet`。要留记录就推到 `KQYaili/crosspet` 的 `grok-cursor-state-order`

## 已知还没做的事

这些不是测试失败：

- Grok 没有睡觉、问好和部分节日图。程序会退回待机。
- Cursor 没有登记「发出消息」「工具刚开始」「子任务开始」这三类钩子：Cursor 会等它们的回答，后两个回答不合格式就拦下工具，没有真 Cursor 验证之前不挂。
- Codex 的 Stop 被别的钩子拦下、同一轮接着干（`stop_hook_active`）时，接着干的那段不演：分不出它和同一轮的迟到事件。
- 前台窗口切换和透明桌宠不在这组测试里。
