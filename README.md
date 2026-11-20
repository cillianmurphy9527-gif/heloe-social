# heloe-social：Heloe 社媒自动化运营仓库

这个仓库是 Heloe（heloe.io）社媒自动化的「大本营」。它保存打法手册、每天的内容计划、封面和视频素材、发布记录和数据，同时用 GitHub Actions 当执行机器人。负责思考和创作的是 Claude 的多角色 Agent（插件 `heloe-social-ops`）。

## 每天怎么运转（北京时间，美东冬令时；夏令时整体提前 1 小时）
| 时间 | 谁 | 做什么 |
|---|---|---|
| 11:30 | GitHub Actions | 从 Buffer 拉取已发帖子的数据 → `data/` |
| 12:00 | GitHub Actions | 抓 Hacker News + Google News 热点 → `trends/` |
| 12:20 | Claude（你的电脑 Chrome，可选） | 扫 Reddit 热帖 → `trends/reddit-*.json` |
| 13:10 | Claude 主编 + 4 个 Agent | 选题 → 写文案 → 做封面和视频 → 品牌审核 → 提交 `content/<日期>/plan.json` |
| 提交后约 5 分钟 | GitHub Actions | 把素材发布到 GitHub Pages → 在 Buffer 排期 |
| 21:30 起 | Buffer | 按美东时间发布：LinkedIn 08:30，X 09:00 / 12:30 / 17:30，Facebook 11:00 |
| 每周一 | Claude 增长分析师 | 复盘数据，更新 `playbook/learnings.md`，把周报发给你 |

## 角色分工
- **主编**（daily-content-run）：定选题和当天排期，统筹各个 Agent，最后提交。
- **选题官**（trend-scout）：抓热点，按热度、相关度、品牌关联度、新鲜度打分。
- **文案**（copywriter）：分别按 LinkedIn、X、Facebook 的写法出稿，配话题标签。
- **设计**（visual-designer）：用品牌模板出封面（PNG）和 15-25 秒动效视频（MP4），出完自己检查一遍画面。
- **品牌审核**（brand-editor）：发布前最后一关。核对数据来源，检查有没有编造内容、语气对不对、话题是否敏感、画面有没有问题。达不到 8 分就不发。
- **增长分析师**（growth-analyst）：每周复盘，调整内容配比、发布时间和规则。

## 一次性设置
1. 在 claude.ai 设置里连接 GitHub。在 GitHub 新建一个空的公开仓库 `heloe-social`，然后由 Claude 把这里的文件推上去。
2. 仓库 **Settings → Pages → Source** 选 **GitHub Actions**。
3. 去 Buffer 创建 API Key：打开 https://publish.buffer.com/settings/api 。然后在仓库 **Settings → Secrets and variables → Actions → New repository secret** 里新建，名字填 `BUFFER_API_KEY`，值填刚才的 Key。**不要把 Key 发到聊天里。**
4. 在仓库 **Actions** 页面手动运行一次 **Setup Buffer**，它会自动找到你在 Buffer 里的三个频道。
5. 在 claude.ai 安装插件 `heloe-social-ops`。可选：连接 Buffer 连接器，这样你可以直接在对话里查看排期、删帖。
6. 定时任务由 Claude 创建：每日内容、每周复盘，可选每日 Reddit 扫描。

## 你可以随时做的事
- **一键暂停**：把 `config/settings.json` 里的 `publishing_enabled` 改成 `false`。也可以直接在对话里说「暂停发布」。
- **补充可公开的公司进展**：写进 `playbook/founder-notes.md`。「Build in Public」类内容只会用这里写过的事实。
- **换品牌素材**：logo 放到 `brand/`，颜色和字体改 `config/brand.json`，所有模板会自动跟着变。

## 目录
```
config/      品牌、频道和发布时段、选题来源、内容支柱、总开关
playbook/    策略与冷启动计划、平台规则、话题标签库、复盘结论、创始人素材
templates/   封面和视频模板（HTML）
render/      渲染器：PNG 封面、MP4 视频、质检拼图
scripts/     抓热点、校验、Buffer 发布、拉数据
content/     每天的选题、文案、审核结果和最终计划
docs/media/  对外托管的素材（GitHub Pages，只保留最近 21 天）
data/        发布记录、各帖数据、表现汇总
plugin/      Claude 插件 heloe-social-ops 的源码
```
